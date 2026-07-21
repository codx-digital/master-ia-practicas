#!/usr/bin/env python3
"""
CP4 — Generador de dataset sintético desde highway-env.

Crea ~5000 pares (observación, acción_steering) usando un policy heurístico
("expert") sobre el entorno highway-v0. Tres splits:

  - train (3500):       densidad estándar, semilla fija → "in-distribution"
  - val_in_dist (750):  misma config, semillas distintas
  - val_ood (750):      densidad de tráfico distinta + más carriles ("OOD")

Output: datasets/cp4-highway-bc.npz con keys:
  - train_obs:        (3500, 84, 84, 3) uint8       (renderizado RGB del entorno)
  - train_actions:    (3500,) float32                (steering normalizado en [-1, 1])
  - val_in_obs:       (750, 84, 84, 3) uint8
  - val_in_actions:   (750,) float32
  - val_ood_obs:      (750, 84, 84, 3) uint8
  - val_ood_actions:  (750,) float32

Determinista: semilla fija → todos los alumnos obtienen el mismo dataset.

Uso:
    python scripts/generate_dataset.py
    python scripts/generate_dataset.py --quick      # 500 train, para iterar rápido
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

# highway-env y gymnasium se importan tarde para dar error legible si faltan
try:
    import gymnasium as gym
    import highway_env  # noqa: F401  (registra los envs)
except ImportError as e:
    raise SystemExit(
        f"Falta dependencia: {e}\n"
        "Ejecuta: pip install -r requirements.txt"
    )


def expert_policy(obs_kin):
    """Policy heurístico ('expert') sobre observación KINEMATICS.

    obs_kin shape: (vehicles, features=5) → [presence, x, y, vx, vy] del ego + 4 vecinos.

    Lógica:
        - Mantener carril si despejado (steering ≈ 0).
        - Si hay vehículo delante muy cerca, cambiar al carril libre.
        - Devuelve steering ∈ [-1, 1] (continuo).
    """
    ego = obs_kin[0]                  # primera fila = ego
    others = obs_kin[1:]              # demás vehículos relativos al ego
    ego_y = ego[2]                    # ya está normalizado por highway-env

    # Detectar coche delante cercano (mismo carril ≈ misma y, x > 0)
    front_threat = False
    for v in others:
        present, dx, dy, _, _ = v
        if present < 0.5:
            continue
        if 0 < dx < 0.20 and abs(dy) < 0.05:
            front_threat = True
            break

    if not front_threat:
        # Volver al centro del carril más probable
        steering = -0.3 * ego_y       # restauración suave
    else:
        # Cambiar al carril contrario al ego_y (heurística simple)
        steering = -0.6 if ego_y >= 0 else 0.6

    return float(np.clip(steering, -1.0, 1.0))


def make_env(config_overrides: dict | None = None, seed: int = 0):
    """Crea highway-v0 con observación visual (grayscale → RGB) + acción continua."""
    base_config = {
        'observation': {
            'type': 'GrayscaleObservation',
            'observation_shape': (84, 84),
            'stack_size': 3,                      # 3 frames apilados → simula contexto
            'weights': [0.2989, 0.5870, 0.1140],  # luminance
            'scaling': 1.75,
        },
        'action': {
            'type': 'ContinuousAction',
            'longitudinal': False,
            'lateral': True,
            'steering_range': [-np.pi / 4, np.pi / 4],
        },
        'lanes_count': 4,
        'vehicles_count': 20,
        'duration': 60,
        'policy_frequency': 5,
        'simulation_frequency': 15,
    }
    if config_overrides:
        base_config.update(config_overrides)

    env = gym.make('highway-v0', config=base_config)
    env.reset(seed=seed)
    return env


def make_kinematics_env(config_overrides: dict | None = None, seed: int = 0):
    """Mismo entorno pero con observación KINEMATICS para que el expert vea otros vehículos.

    Truco: corremos DOS entornos en paralelo con misma semilla — uno KINEMATICS
    (para el expert) y otro GRAYSCALE (para guardar la observación que verá la CNN).
    Esto es la convención clásica de BC con teacher heurístico + observación visual.
    """
    base_config = {
        'observation': {
            'type': 'Kinematics',
            'vehicles_count': 5,
            'features': ['presence', 'x', 'y', 'vx', 'vy'],
            'normalize': True,
        },
        'action': {'type': 'ContinuousAction', 'longitudinal': False, 'lateral': True,
                   'steering_range': [-np.pi / 4, np.pi / 4]},
        'lanes_count': 4,
        'vehicles_count': 20,
        'duration': 60,
        'policy_frequency': 5,
        'simulation_frequency': 15,
    }
    if config_overrides:
        base_config.update(config_overrides)

    env = gym.make('highway-v0', config=base_config)
    env.reset(seed=seed)
    return env


def collect_split(n_samples: int, base_seed: int, ood: bool, verbose: bool = True):
    """Recolecta n_samples pares (obs_visual, steering) con el expert policy."""
    visual_obs, steerings = [], []

    # Si OOD, cambiar densidad + carriles
    overrides = {}
    if ood:
        overrides = {'lanes_count': 3, 'vehicles_count': 35, 'duration': 60}

    seed = base_seed
    pbar_step = max(1, n_samples // 20)

    while len(steerings) < n_samples:
        # Crear pareja KINEMATICS (expert decide) + VISUAL (lo que ve la CNN)
        env_kin = make_kinematics_env(overrides, seed=seed)
        env_vis = make_env(overrides, seed=seed)
        obs_k, _ = env_kin.reset(seed=seed)
        obs_v, _ = env_vis.reset(seed=seed)

        done = trunc = False
        while not (done or trunc):
            steer = expert_policy(obs_k)

            # GRAYSCALE devuelve shape (stack_size, H, W) — lo pasamos a (H, W, 3)
            if obs_v.ndim == 3 and obs_v.shape[0] == 3:
                obs_save = np.transpose(obs_v, (1, 2, 0))
            else:
                obs_save = obs_v
            obs_save = obs_save.astype(np.uint8)
            visual_obs.append(obs_save)
            steerings.append(steer)

            # acción continuo: highway-env espera vector [steering]
            action_continuous = np.array([steer], dtype=np.float32)
            obs_k, _, done_k, trunc_k, _ = env_kin.step(action_continuous)
            obs_v, _, done_v, trunc_v, _ = env_vis.step(action_continuous)
            done = done_k or done_v
            trunc = trunc_k or trunc_v

            if len(steerings) >= n_samples:
                break

            if verbose and len(steerings) % pbar_step == 0:
                sys.stdout.write(f"\r  {'OOD' if ood else 'in-dist':>8s}  {len(steerings):>5d}/{n_samples}")
                sys.stdout.flush()

        env_kin.close()
        env_vis.close()
        seed += 1

    if verbose:
        sys.stdout.write("\n")

    return np.array(visual_obs[:n_samples], dtype=np.uint8), np.array(steerings[:n_samples], dtype=np.float32)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--quick', action='store_true', help='Solo 500/100/100 para iteración rápida')
    parser.add_argument('--output', default='datasets/cp4-highway-bc.npz')
    args = parser.parse_args()

    if args.quick:
        N_TRAIN, N_VAL_IN, N_VAL_OOD = 500, 100, 100
    else:
        N_TRAIN, N_VAL_IN, N_VAL_OOD = 3500, 750, 750

    print(f'CP4 — Generando dataset sintético desde highway-env')
    print(f'      train:     {N_TRAIN}')
    print(f'      val_in:    {N_VAL_IN}')
    print(f'      val_ood:   {N_VAL_OOD}')
    print()

    print('1) Recolectando split TRAIN (seed=100)...')
    train_obs, train_actions = collect_split(N_TRAIN, base_seed=100, ood=False)

    print('\n2) Recolectando split VAL in-distribution (seed=2000)...')
    val_in_obs, val_in_actions = collect_split(N_VAL_IN, base_seed=2000, ood=False)

    print('\n3) Recolectando split VAL OOD (seed=3000)...')
    val_ood_obs, val_ood_actions = collect_split(N_VAL_OOD, base_seed=3000, ood=True)

    # Guardar
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_path,
        train_obs=train_obs, train_actions=train_actions,
        val_in_obs=val_in_obs, val_in_actions=val_in_actions,
        val_ood_obs=val_ood_obs, val_ood_actions=val_ood_actions,
    )

    size_mb = out_path.stat().st_size / 1e6
    print(f'\n✅ Dataset guardado en {out_path}  ({size_mb:.1f} MB)')
    print(f'   train     shape={train_obs.shape}, steering mean={train_actions.mean():+.3f}, std={train_actions.std():.3f}')
    print(f'   val_in    shape={val_in_obs.shape}, steering mean={val_in_actions.mean():+.3f}, std={val_in_actions.std():.3f}')
    print(f'   val_ood   shape={val_ood_obs.shape}, steering mean={val_ood_actions.mean():+.3f}, std={val_ood_actions.std():.3f}')


if __name__ == '__main__':
    main()
