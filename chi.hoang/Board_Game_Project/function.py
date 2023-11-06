import pandas as pd
import numpy as np

def Bayesian_average_function(row):
    n = row['rating_number']
    m = row['rating_average']
    bayesian_avg = (prior_weight*prior_mean + m*n)/(prior_weight+n)
    return bayesian_avg





































