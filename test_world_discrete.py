#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from particlefilter import ParticleFilter

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
    sigma = 1
    expected_state = state + prop_param
    return int(np.random.normal(expected_state, sigma))

n_particles = int(input('Number of particles: '))

pf = ParticleFilter(
    p_particle,
    next_particle,
    np.random.choice(100, size=n_particles)
)

all_states = list(range(100))
true_obs = [get_true_obs(state) for state in all_states]
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
env_plt, = ax.plot(all_states, true_obs, lw=5, zorder=1)

true_state = 10
print(get_true_obs(true_state))
true_plt, = ax.plot([true_state, true_state], [70, get_true_obs(true_state)], '.-', ms=20, zorder=3)

particles_plt, = ax.plot(pf.particles, [70] * n_particles, '.', ms=20, zorder=2, alpha=0.2)

plt.ylim([0, 80])
plt.show(block=False)

while True:
    obs = np.random.normal(get_true_obs(true_state), 2)

    print('True state: {}'.format(true_state))
    true_plt.set_xdata([true_state, true_state])
    true_plt.set_ydata([70, obs])
    print('Particles: {}'.format(sorted(pf.particles)))
    particles_plt.set_xdata(pf.particles)
    print('=========\n')
    fig.canvas.draw()

    print('Observation: {}'.format(obs))
    prop_param = int(input('Enter expected change in state: '))
    true_state = max(min(true_state + prop_param, 99), 0)

    pf.observe(obs, prop_param)