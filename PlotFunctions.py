import pandas as pd
import matplotlib.pyplot as plt


class PlotFunctions:

    @staticmethod
    def plot_population(population):
        df = pd.DataFrame(population)
        plt.scatter(*zip(list(df.columns)))
