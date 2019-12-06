import pandas as pd
import matplotlib.pyplot as plt
import Parameters as par
import numpy as np
import os


class PlotWindow:

    def __init__(self):
        self.list_of_dead = []
        self.plot_columns = int(np.sum(np.array([par.plot_grid, par.plot_proportions])))
        if self.plot_columns == 2:
            self.fig_size = (14, 4.8)
        elif self.plot_columns == 1:
            self.fig_size = (6.4, 4.8)

    def add_dead(self, location_of_dead):
        self.list_of_dead.append(location_of_dead)

    def update_simulation_plot(self, population, time_step, day, population_count):
        if self.plot_columns > 0:
            fig, axs = plt.subplots(nrows=1, ncols=self.plot_columns, figsize=self.fig_size)
            fig.suptitle('t = {}'.format(time_step), y=0.99)
            if self.plot_columns > 1:
                self.update_grid_plot(axs[0], population, day)
                self.update_proportion_plot(axs[1])
            elif par.plot_grid:
                self.update_grid_plot(axs, population, day)
            elif par.plot_proportions:
                self.update_proportion_plot(axs)
            path = os.path.join(par.save_path, 't{}'.format(time_step))
            plt.savefig(path)
            plt.close()

    def update_grid_plot(self, ax, population, day):
        if not day:
            ax.set_facecolor('xkcd:grey')
        self.plot_the_dead(ax)
        PlotWindow.plot_population(ax, population)
        PlotWindow.plot_airports(ax)
        PlotWindow.plot_boundaries(ax)
        ax.set(xlim=(0, par.dimension), ylim=(0, par.dimension))
        # plt.axis('off')
        ax.legend(bbox_to_anchor=(0., 0.98, 1., 0.102), loc="upper left", mode='expand',
                  ncol=4, borderaxespad=0., frameon=False)

    def update_proportion_plot(self, ax):
        return 0

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
        ax.scatter(df_s['x'], df_s['y'], c='C0', label='Susceptible', s=10)
        ax.scatter(df_r['x'], df_r['y'], c='C2', label='Recovered', s=8)
        ax.scatter(df_e['x'], df_e['y'], c='C3', label='Exposed', s=6)
        ax.scatter(df_i['x'], df_i['y'], c='C1', label='Symptomatic', s=4)

    def plot_the_dead(self, ax):
        dead = np.array(self.list_of_dead)
        if not dead.size == 0:
            ax.scatter(dead[:, 0], dead[:, 1], marker="x", c='C7', s=12)

    @staticmethod
    def plot_airports(ax):
        if par.n_airport > 0:
            airports = np.array(par.airport_location)
            ax.scatter(airports[:, 0], airports[:, 1], marker="s", edgecolors='black', facecolors='none')

    @staticmethod
    def plot_boundaries(ax):
        # Inside boundaries
        ax.plot([par.boundary, par.boundary], [0, par.dimension], c='black', linewidth=2)
        ax.plot([0, par.dimension], [par.boundary, par.boundary], c='black', linewidth=2)
        # Outside boundaries
        ax.plot([0, 0], [0, par.dimension], c='black', linewidth=4)
        ax.plot([par.dimension, par.dimension], [0, par.dimension], c='black', linewidth=4)
        ax.plot([0, par.dimension], [0, 0], c='black', linewidth=4)
        ax.plot([0, par.dimension], [par.dimension, par.dimension], c='black', linewidth=4)


# TODO
# ***Day and night, color background, possibly with scale
# (ELLA) Fix legend
# ***Mark dead by cross
# ***Mark airports
# ***Implement and mark walls
# ***Infected --> exposed and symptomatic
# ---Count down until symptomatic
# ---Hospitals?
# (HAODONG) Not infect every individual in one grid
# ---More individual behaviors,
# ---Avoid symptomatic areas
# (HAODONG) Higher probability of infecting when symptomatic
# "Shut down" airport if some procentage of
# html instead of gif
# continuous coordinates

