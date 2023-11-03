import pandas as pd
import numpy as np
import matplotlib_inline as plt


def Bayesian_average_funct(row):
        n = row['rating_number']
        m = row['rating_average']
        bayesian_avg = (prior_weight * prior_mean + n*m) / (prior_weight + n)
        return bayesian_avg

full_table['bayesian_average'] = full_table.apply(lambda row: Bayesian_average_funct(row),axis=1)




plt.hist(full_table['bayesian_average'],
         bins=20, alpha=0.5
         label='Bayesian Average')
plt.xlable('Bayesian Average')
plt.ylable('Distribution of Bayesian Average Scores')
plt.legend()
























