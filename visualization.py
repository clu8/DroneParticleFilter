import matplotlib.pyplot as plt
import seaborn as sns

class ParticleFilterVisualization(object):
    def __init__(self, plot_states, get_true_obs, particles, y_particle, true_state=None):
        self.y_particle = y_particle

        self.fig = plt.figure()
        ax = self.fig.add_subplot(1, 1, 1)

        true_obs = [get_true_obs(state) for state in plot_states]
        self.env_plt, = ax.plot(plot_states, true_obs, lw=5, zorder=1)

        self.obs_plt, = ax.plot([plot_states[0], plot_states[-1]],
                                [self.y_particle, self.y_particle],
                                '--', lw=3, zorder=2)

        self.particles_plt, = ax.plot(particles, [self.y_particle] * len(particles),
                                      '.', ms=20, alpha=0.2, zorder=2)

        if true_state:
            self.true_state_plt, = ax.plot([true_state, true_state],
                                           [self.y_particle, get_true_obs(true_state)],
                                           '.-', ms=20, zorder=3)

        plt.ylim([0, int(y_particle * 1.1)])
        plt.show(block=False)

    def update(self, particles, obs, true_state=None):
        self.particles_plt.set_xdata(particles)
        self.obs_plt.set_ydata([obs, obs])
        if true_state:
            self.true_state_plt.set_xdata([true_state, true_state])
            self.true_state_plt.set_ydata([self.y_particle, obs])

        self.fig.canvas.draw()
