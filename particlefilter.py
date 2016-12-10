import numpy as np

class ParticleFilter(object):
    def __init__(self, p_particles, next_particles, initial_particles):
        """
        p_particle: function where p_particle(states, sensor_reading)
            returns probability of all particles
        next_particles: function where next_particles(states, prop_param)
            samples particles at next time step
        initial_particles: iterable of initial particles
        """
        self.p_particles = p_particles
        self.next_particles = next_particles
        self.particles = np.array(initial_particles)

    def observe(self, sensor_reading, prop_param):
        """
        Observe a sensor reading, reweight and resample particles, and then propogate in time.
        """
        # reweight
        weights = self.p_particles(self.particles, sensor_reading)
        weights /= sum(weights)

        # resample & propogate in time
        self.particles = self.next_particles(
            np.random.choice(self.particles, size=len(self.particles), p=weights),
            prop_param
        )

    def get_state_belief(self):
        """
        Returns Counter mapping state -> belief probability using current particle states.
        """
        return {state: count / len(self.particles)
                for state, count in Counter(self.particles)}