#!/usr/bin/env python3

from collections import Counter
import numpy as np

class ParticleFilter(object):
    def __init__(self, state_to_true, p_particle, next_particle, n_particles=200):
        """
        state_to_true: dict mapping states to true sensor reading value
        p_particle: function where p_particle(true_reading, sensor_reading)
            returns probability of particle
        next_particle: function where next_particle(state, prop_param)
            samples particle at next time step
        """
        self.state_to_true = state_to_true
        self.states = list(state_to_true.keys())
        self.p_particle = p_particle
        self.next_particle = next_particle
        self.n_particles = n_particles

        self.particles = Counter(np.random.choice(self.states, size=self.n_particles))

    def observe(self, sensor_reading, prop_param):
        """
        Observe a sensor reading, reweight and resample particles, and then propogate in time.
        """
        # reweight
        for state in self.particles:
            self.particles[state] *= self.p_particle(self.state_to_true[state], sensor_reading)

        # resample
        total_weight = sum(self.particles.values())
        weights = [self.particles[state] / total_weight for state in self.states]
        resampled = np.random.choice(self.states, size=self.n_particles, p=weights)

        # propogate in time
        self.particles = Counter(self.next_particle(state, prop_param) for state in resampled)

    def get_state_belief(self):
        """
        Returns dict mapping state -> belief probability using current particle states.
        """
        return {state: self.particles[state] / self.n_particles for state in self.states}
