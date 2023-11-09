import pandas as pd

def Function_Bayesian_Average(row):
    m = row['rating_average']
    n = row['rating_number']
    bayesian_avg = (prior_mean*prior_weight + m*n)/(prior_weight+n)
    return bayesian_avg












































