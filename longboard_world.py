#!/usr/bin/env python3

import csv

import numpy as np

from particlefilter import ParticleFilter
from visualization import ParticleFilterVisualization

with open('longboard_map.csv') as f:
    environment = {i: float(line) for i, line in enumerate(f.readlines())}

def get_true_obs(state):
    return environment[state]

def p_particle(state, obs):
    """
    Weight using Gaussian kernel
    """
    # variance = 0.207**2 # empirically tested variance
    variance = 5 # larger variance to test limits
    return np.exp(-(get_true_obs(state) - obs) ** 2 / (2 * variance)) \
        if state in environment else 0

def next_particle(state, prop_param):
    """
    Sample new state from Gaussian around new expected location. 
    prop_param: expected change in feet
    """
    expected_state = state + prop_param * 4
    # stdev = prop_param * 4 # guesstimate of noise
    stdev = prop_param * 10 # larger variance to test limits
    return int(np.round(np.random.normal(expected_state, stdev)))

n_particles = int(input('Number of particles: '))

pf = ParticleFilter(
    p_particle,
    next_particle,
    np.random.choice(66, size=n_particles)
)

all_states = list(range(66))
viz = ParticleFilterVisualization(all_states, get_true_obs, pf.particles,
                                  y_particle=120)
with open('longboard_episode_2.csv') as csvfile:
    reader = csv.reader(csvfile)
    prev_pos = 5
    for row_idx, row in enumerate(reader):
        if row_idx % 100 == 0: # sample every 100 row to avoid tiny transitions
            obs, pos, _ = map(float, row)

            print('Particles: {}'.format(np.round(sorted(pf.particles), 2)))
            print('=========\n')
            viz.update(pf.particles, obs)
            input('Press [enter] to go to next time step')

            prop_param = pos - prev_pos
            print('Observation: {}'.format(obs))
            print('Change in position: {}'.format(prop_param))
            prev_pos = pos

            pf.observe(obs, prop_param)