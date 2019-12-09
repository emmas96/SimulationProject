import pandas as pd
import matplotlib.pyplot as plt
import Parameters as par
import numpy as np
import os


class PlotWindow:

    def __init__(self):
        self.list_of_dead = []
        self.health_states_short = ['s', 'e', 'i', 'r']
        self.health_states = ['Susc.', 'Exp.', 'Symp.', 'Rec.', 'Dead']
        self.coloring = ['C0', 'C3', 'C1', 'C2', 'C7']
        self.population_count = {'Susc.': [], 'Exp.': [], 'Symp.': [], 'Rec.': [], 'Dead': []}
        self.plot_columns = int(np.sum(np.array([par.plot_grid, par.plot_proportions])))
        if self.plot_columns == 2:
            self.fig_size = (14, 4.8)
        elif self.plot_columns == 1:
            self.fig_size = (6.4, 4.8)

    def add_dead(self, location_of_dead):
        self.list_of_dead.append(location_of_dead)

    def update_population_count(self, current_population_count):
        for i in range(len(self.health_states)):
            if i == len(self.health_states) - 1:
                self.population_count['Dead'].append(len(self.list_of_dead))
            else:
                self.population_count[self.health_states[i]].append(current_population_count[self.health_states_short[i]])

    def update_simulation_plot(self, population, time_step, day):
        if self.plot_columns > 0:
            fig, axs = plt.subplots(nrows=1, ncols=self.plot_columns, figsize=self.fig_size)
            if self.plot_columns > 1:
                self.update_grid_plot(axs[0], population, day)
                self.update_proportion_plot(axs[1])
            elif par.plot_grid:
                fig.suptitle('t = {}'.format(time_step), y=0.99)
                self.update_grid_plot(axs, population, day)
            elif par.plot_proportions:
                self.update_proportion_plot(axs)
            path = os.path.join(par.save_path, 't{}'.format(time_step))
            plt.savefig(path)
            plt.close()

    def update_grid_plot(self, ax, population, day):
        if not day:
            ax.set_facecolor('xkcd:grey')
        h_dead = self.plot_the_dead(ax)
        h_s, h_r, h_e, h_i = PlotWindow.plot_population(ax, population)
        h_air = PlotWindow.plot_airports(ax)
        h_bound = PlotWindow.plot_boundaries(ax)
        ax.set(xlim=(0, par.dimension), ylim=(0, par.dimension))
        # plt.axis('off')
        ax.legend(bbox_to_anchor=(0., 1.02, 1., 0.102), loc="upper left", mode='expand',
                  ncol=4, borderaxespad=0., frameon=False)

    def update_proportion_plot(self, ax):
        for i in range(len(self.health_states)):
            health = self.health_states[i]
            ax.plot(self.population_count[health], label=health, c=self.coloring[i])
        if par.limited_time:
            ax.set(xlim=(0, par.T))
        ax.legend(bbox_to_anchor=(0., 0.98, 1., 0.102), loc="upper left", mode='expand',
                  ncol=5, borderaxespad=0., frameon=False)

    @staticmethod
    def plot_population(ax, population):
        df = pd.DataFrame.from_dict(population, orient='index')
        df = df[df['count'] > 0]
        df['x'] = [int(data[0]) for data in df.index]
        df['y'] = [int(data[1]) for data in df.index]
        df_s = df[(df['s'].str.len() != 0)]
        df_e = df[(df['e'].str.len() != 0)]
        df_i = df[(df['i'].str.len() != 0)]
        df_r = df[(df['r'].str.len() != 0)]
        h_s = ax.scatter(df_s['x'], df_s['y'], c='C0', label='Susceptible', s=10)
        h_r = ax.scatter(df_r['x'], df_r['y'], c='C2', label='Recovered', s=8)
        h_e = ax.scatter(df_e['x'], df_e['y'], c='C3', label='Exposed', s=6)
        h_i = ax.scatter(df_i['x'], df_i['y'], c='C1', label='Symptomatic', s=4)
        return h_s, h_r, h_e, h_i

    def plot_the_dead(self, ax):
        dead = np.array(self.list_of_dead)
        if not dead.size == 0:
            return ax.scatter(dead[:, 0], dead[:, 1], marker="x", c='C7', s=12, label='Dead')
        return None

    @staticmethod
    def plot_airports(ax):
        if par.n_airport > 0:
            airports = np.array(par.airport_location)
            return ax.scatter(airports[:, 0], airports[:, 1], marker="s", edgecolors='black', facecolors='none',
                              label='Airports')
        return None

    @staticmethod
    def plot_boundaries(ax):
        # Inside boundaries
        label = 'Area boundary'
        if par.boundary == 0:
            label = None
        h_bound = ax.plot([par.boundary-0.5, par.boundary-0.5], [0, par.dimension], c='black', linewidth=2, label=label)
        ax.plot([0, par.dimension], [par.boundary-0.5, par.boundary-0.5], c='black', linewidth=2)
        # Outside boundaries
        ax.plot([0, 0], [0, par.dimension], c='black', linewidth=4)
        ax.plot([par.dimension, par.dimension], [0, par.dimension], c='black', linewidth=4)
        ax.plot([0, par.dimension], [0, 0], c='black', linewidth=4)
        ax.plot([0, par.dimension], [par.dimension, par.dimension], c='black', linewidth=4)
        return h_bound

