import matplotlib.pyplot as plt
import numpy as np

%matplotlib_inline

x = full_table['rating_number']
y = full_table['rating_average']
z = full_table['bayesian_average']

# scatter plot of "Game ranking based on Average scores"
def average_plot(x, y, x_label, y_label, title, color):
    plt.figure(figsize=(8,6))
    plt.scatter(x,y, color='b', label="Data Points")
    plt.xlabel('Number of votes')
    plt.ylabel('Average scores')
    plt.title('Game ratings based on Average score')
    plt.legend()
    plt.grid(True)
    plt.show()

# scatter plot of "Game rankings based on Bayesian average score"
def bayesian_average_plot(x, z, x_label, z_label, title, color):
    plt.figure(figsize=(8,6))
    plt.scatter(x,z, color='b', label="Data Points")
    plt.xlabel('Number of votes')
    plt.ylabel('Bayesian Average scores')
    plt.title('Game ratings based on Bayesian Average score')
    plt.legend()
    plt.grid(True)
    plt.show()



