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
    variance = 10
    return np.exp(-(get_true_obs(state) - obs) ** 2 / (2 * variance)) \
        if 0 < state < 100 else 0

def next_particle(state, prop_param):
    """
    Sample new state from Gaussian around new expected location. 
    prop_param: predicted change in state
    """
    expected_state = state + prop_param
    return np.random.normal(expected_state, abs(prop_param) ** 0.5)

n_particles = int(input('Number of particles: '))

pf = ParticleFilter(
    p_particle,
    next_particle,
    100 * np.random.random(n_particles)
)

plot_states = np.linspace(0, 100, 201)
true_state = 10
viz = ParticleFilterVisualization(plot_states, get_true_obs, pf.particles,
                                  y_particle=700, true_state=true_state)

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