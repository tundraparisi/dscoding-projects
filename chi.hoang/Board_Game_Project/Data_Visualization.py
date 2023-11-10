import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_csv('Average_table.csv')
df2 = pd.read_csv('Bayesian_table.csv')


class DataVisualization:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def plot_average_ranking(self):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.x, self.y, color='b')
        plt.xlabel('Number of votes')
        plt.ylabel('Average scores')
        plt.title('Game ratings based on Average score')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_bayesian_ranking(self):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.x, self.z, color='b')
        plt.xlabel('Number of votes')
        plt.ylabel('Bayesian Average scores')
        plt.title('Game ratings based on Bayesian Average score')
        plt.legend()
        plt.grid(True)
        plt.show()


x = df1['rating_number']
y = df1['rating_average']
z = df2['bayesian_average']
