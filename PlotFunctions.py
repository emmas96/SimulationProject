import pandas as pd
import matplotlib.pyplot as plt


class PlotFunctions:

    @staticmethod
    def plot_population(population, path):
        df = pd.DataFrame.from_dict(population, orient='index')
        df = df[df['count'] > 0]
        df['x'] = [int(data[0]) for data in df.index]
        df['y'] = [int(data[1]) for data in df.index]
        df_s = df[(df['s'].str.len() != 0)]
        df_i = df[(df['i'].str.len() != 0)]
        df_r = df[(df['r'].str.len() != 0)]
        plt.scatter(df_s['x'], df_s['y'], c='C0', label='Susceptible')
        plt.scatter(df_i['x'], df_i['y'], c='C1', label='Infected')
        plt.scatter(df_r['x'], df_r['y'], c='C2', label='Recovered')
        plt.savefig(path)
        plt.close()



