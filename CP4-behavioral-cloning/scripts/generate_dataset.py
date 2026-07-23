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


STEER_MAX = np.pi / 4   # coincide con steering_range del env


def expert_steer(vehicle, network, target_lane_index, k_lat=4.0, k_head=0.7):
    """Policy 'expert' de mantenimiento de carril usando el ESTADO REAL del coche.

    En vez de depender de una observación normalizada (frágil entre versiones de
    highway-env), controlamos directamente con la geometría: llevamos el coche al
    centro del carril objetivo corrigiendo (a) su desviación lateral y (b) su rumbo.
    Es un controlador tipo Stanley simplificado.

    Devuelve steering ∈ [-1, 1] (se mapea al steering_range del env).
    """
    lane = network.get_lane(target_lane_index)
    longitudinal, lateral = lane.local_coordinates(vehicle.position)
    lane_heading = lane.heading_at(longitudinal)
    heading_err = (vehicle.heading - lane_heading + np.pi) % (2 * np.pi) - np.pi
    angle = -k_head * heading_err - np.arctan2(k_lat * lateral, max(vehicle.speed, 3.0))
    return float(np.clip(angle / STEER_MAX, -1.0, 1.0))


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


LANE_CHANGE_PERIOD = 8   # cada ~8 pasos el expert decide un cambio de carril → da variedad de steering


def collect_split(n_samples: int, base_seed: int, ood: bool, verbose: bool = True):
    """Recolecta n_samples pares (obs_visual, steering) con el expert de mantenimiento de carril.

    Usamos UN solo entorno (grayscale = lo que ve la CNN) y leemos el estado real del
    coche (`env.unwrapped.vehicle`) para que el expert lo mantenga en la carretera.
    El expert va cambiando de carril objetivo cada pocos pasos para generar giros.
    """
    visual_obs, steerings = [], []

    # Si OOD, cambiar densidad + carriles
    overrides = {}
    if ood:
        # OOD = geometría NO vista en train (5 carriles vs 4) + otra densidad de tráfico.
        # Con 5 carriles la variedad de giro es ~la de train, así que el gap in-dist vs OOD
        # refleja la GENERALIZACIÓN a geometría nueva (no solo un cambio de distribución de acciones).
        overrides = {'lanes_count': 5, 'vehicles_count': 30, 'duration': 60}

    rng = np.random.default_rng(base_seed)   # decisiones de cambio de carril → deterministas
    seed = base_seed
    pbar_step = max(1, n_samples // 20)

    while len(steerings) < n_samples:
        env = make_env(overrides, seed=seed)
        obs, _ = env.reset(seed=seed)
        network = env.unwrapped.road.network
        veh = env.unwrapped.vehicle
        _from, _to, lane_id = veh.lane_index
        n_lanes = len(network.graph[_from][_to])
        target_lane = lane_id
        step_i = 0

        done = trunc = False
        while not (done or trunc):
            veh = env.unwrapped.vehicle
            _from, _to, _ = veh.lane_index
            step_i += 1

            # cambio de carril deliberado cada LANE_CHANGE_PERIOD pasos (dentro de la calzada)
            if step_i % LANE_CHANGE_PERIOD == 0:
                nxt = target_lane + (1 if rng.random() < 0.5 else -1)
                if 0 <= nxt < n_lanes:
                    target_lane = nxt

            steer = expert_steer(veh, network, (_from, _to, target_lane))

            # GRAYSCALE devuelve shape (stack_size, H, W) — lo pasamos a (H, W, 3)
            if obs.ndim == 3 and obs.shape[0] == 3:
                obs_save = np.transpose(obs, (1, 2, 0))
            else:
                obs_save = obs
            visual_obs.append(obs_save.astype(np.uint8))
            steerings.append(steer)

            obs, _, done, trunc, _ = env.step(np.array([steer], dtype=np.float32))

            if len(steerings) >= n_samples:
                break

            if verbose and len(steerings) % pbar_step == 0:
                sys.stdout.write(f"\r  {'OOD' if ood else 'in-dist':>8s}  {len(steerings):>5d}/{n_samples}")
                sys.stdout.flush()

        env.close()
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
