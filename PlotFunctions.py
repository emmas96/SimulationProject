import pandas as pd
import matplotlib.pyplot as plt
import Parameters as par
import numpy as np


class PlotFunctions:

    @staticmethod
    def plot_population(population, path, time, day):
        df_s, df_i, df_r = PlotFunctions.extract_individuals(population)
        fig, ax = plt.subplots(1, 1)
        fig.suptitle('t = {}'.format(time))
        # Change background color depending on day and night
        if not day:
            ax.figure.set_facecolor('xkcd:black')
            ax.set_facecolor('xkcd:gray')
        # Plot individuals
        ax.scatter(df_s['x'], df_s['y'], c='C0', label='Susceptible', s=7)
        ax.scatter(df_r['x'], df_r['y'], c='C2', label='Recovered', s=5)
        ax.scatter(df_i['x'], df_i['y'], c='C1', label='Infected', s=3)
        # Dead people
        ax.plot([10], [20], marker="x", c='black')
        # Airports
        airports = np.array(par.airport_location)
        ax.plot(airports[:, 1], airports[:, 2], marker="s", c='black', fillstyle='none')
        # Walls
        ax.plot([par.cross_wall_coordinate, par.cross_wall_coordinate], [0, par.dimension], c='black', linewidth=2)
        ax.plot([0, par.dimension], [par.cross_wall_coordinate, par.cross_wall_coordinate], c='black', linewidth=2)

        ax.set(xlim=(0, par.dimension), ylim=(0, par.dimension))
        plt.legend(bbox_to_anchor=(0., 1.02, 1., 0.102), loc="upper left", mode='expand', ncol=3, borderaxespad=0.)
        plt.savefig(path)
        plt.close()

    @staticmethod
    def extract_individuals(population):
        df = pd.DataFrame.from_dict(population, orient='index')
        df = df[df['count'] > 0]
        df['x'] = [int(data[0]) for data in df.index]
        df['y'] = [int(data[1]) for data in df.index]
        return df[(df['s'].str.len() != 0)], df[(df['i'].str.len() != 0)], df[(df['r'].str.len() != 0)]


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
# Higher probability of infecting when symptomatic
# "Shut down" airport if some procentage of
# html instead of gif

