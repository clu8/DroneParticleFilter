#!/usr/bin/env python3

import numpy as np

from particlefilter import ParticleFilter
from visualization import ParticleFilterVisualization

with open('longboard_map.txt') as f:
    environment = {i: float(line) for i, line in enumerate(f.readlines())

def get_true_obs(state):
    return environment[state]

def p_particle(state, obs):
    """
    Weight using Gaussian kernel
    """
    variance = 0.207**2
    return np.exp(-(get_true_obs(state) - obs) ** 2 / (2 * variance)) \
        if 0 < state < 100 else 0

def next_particle(state, prop_param):
    """
    Sample new state from Gaussian around new expected location. 
    prop_param: expected change in feet
    """
    expected_state = state + prop_param * 4
    return np.random.normal(expected_state, abs(prop_param) ** 0.5)

n_particles = int(input('Number of particles: '))

pf = ParticleFilter(
    p_particle,
    next_particle,
    np.random.choice(66, size=n_particles)
)

all_states = list(range(66))
viz = ParticleFilterVisualization(all_states, get_true_obs, pf.particles,
                                  y_particle=700)

while True:
    obs = np.random.normal(get_true_obs(true_state), 5)

    print('True state: {}'.format(true_state))
    print('Particles: {}'.format(np.round(sorted(pf.particles), 2)))
    print('=========\n')
    viz.update(pf.particles, obs, true_state)

    print('Observation: {}'.format(obs))
    prop_param = float(input('Enter expected change in state: '))
    true_state = max(min(true_state + prop_param, 99), 0)

    pf.observe(obs, prop_param)