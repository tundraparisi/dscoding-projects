import pandas as pd
import numpy as np
import matplotlib_pyplot as plt

def Bayesian_average_funct(row):
        n = row['rating_number']
        m = row['rating_average']
        bayesian_avg = (prior_weight * prior_mean + n*m) / (prior_weight + n)
        return bayesian_avg


























