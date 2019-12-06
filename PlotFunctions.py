import pandas as pd
import matplotlib.pyplot as plt
import Parameters as par
import numpy as np


class PlotFunctions:

    @staticmethod
    def plot_population(population, dead, path, time, day):
        df_s, df_e, df_i, df_r = PlotFunctions.extract_individuals(population)
        fig, ax = plt.subplots(1, 1)
        fig.suptitle('t = {}'.format(time), y=0.99)
        # Change background color depending on day and night
        if not day:
            #ax.figure.set_facecolor('black')
            ax.set_facecolor('xkcd:grey')

        # Dead people
        if not dead.size == 0:
            ax.scatter(dead[:, 0], dead[:, 1], marker="x", c='C7', s=12)
        # Plot individuals
        ax.scatter(df_s['x'], df_s['y'], c='C0', label='Susceptible', s=10)
        ax.scatter(df_r['x'], df_r['y'], c='C2', label='Recovered', s=8)
        ax.scatter(df_e['x'], df_e['y'], c='C3', label='Exposed', s=6)
        ax.scatter(df_i['x'], df_i['y'], c='C1', label='Symptomatic', s=4)
        # Airports
        if par.n_airport > 0:
            airports = np.array(par.airport_location)
            ax.scatter(airports[:, 0], airports[:, 1], marker="s", edgecolors='black', facecolors='none')
        # Inside boundaries
        ax.plot([par.boundary, par.boundary], [0, par.dimension], c='black', linewidth=2)
        ax.plot([0, par.dimension], [par.boundary, par.boundary], c='black', linewidth=2)
        # Outside boundaries
        ax.plot([0, 0], [0, par.dimension], c='black', linewidth=4)
        ax.plot([par.dimension, par.dimension], [0, par.dimension], c='black', linewidth=4)
        ax.plot([0, par.dimension], [0, 0], c='black', linewidth=4)
        ax.plot([0, par.dimension], [par.dimension, par.dimension], c='black', linewidth=4)

        ax.set(xlim=(0, par.dimension), ylim=(0, par.dimension))
        #plt.axis('off')
        plt.legend(bbox_to_anchor=(0., 0.98, 1., 0.102), loc="upper left", mode='expand',
                   ncol=4, borderaxespad=0., frameon=False)
        plt.savefig(path)
        plt.close()

    @staticmethod
    def extract_individuals(population):
        df = pd.DataFrame.from_dict(population, orient='index')
        df = df[df['count'] > 0]
        df['x'] = [int(data[0]) for data in df.index]
        df['y'] = [int(data[1]) for data in df.index]
        return df[(df['s'].str.len() != 0)], df[(df['e'].str.len() != 0)], \
               df[(df['i'].str.len() != 0)], df[(df['r'].str.len() != 0)]


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
# (EMMA) continuous coordinates

