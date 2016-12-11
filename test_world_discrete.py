#!/usr/bin/env python3

import numpy as np

from particlefilter import ParticleFilter
from visualization import ParticleFilterVisualization

def get_true_obs(state):
    if state < 20:
        return 10
    elif 20 <= state < 60:
        return state
    elif 60 <= state < 80:
        return 10
    else:
        return 20

def p_particle(state, sensor_reading):
    """
    Weight using Gaussian kernel
    """
    variance = 20
    return np.exp(-(get_true_obs(state) - sensor_reading) ** 2 / (2 * variance)) \
        if 0 <= state < 100 else 0

def next_particle(state, prop_param):
    """
    Sample new state from Gaussian around new expected location. 
    prop_param: predicted change in state
    """
    expected_state = state + prop_param
    return int(np.random.normal(expected_state, abs(prop_param) ** 0.5))

n_particles = int(input('Number of particles: '))

pf = ParticleFilter(
    p_particle,
    next_particle,
    np.random.choice(100, size=n_particles)
)

all_states = list(range(100))
true_state = 10
viz = ParticleFilterVisualization(all_states, get_true_obs, pf.particles,
                                  y_particle=70, true_state=true_state)

while True:
    obs = np.random.normal(get_true_obs(true_state), 2)

    print('True state: {}'.format(true_state))
    print('Particles: {}'.format(sorted(pf.particles)))
    print('=========\n')
    viz.update(pf.particles, obs, true_state)

    print('Observation: {}'.format(obs))
    prop_param = int(input('Enter expected change in state: '))
    true_state = max(min(true_state + prop_param, 99), 0)

    pf.observe(obs, prop_param)