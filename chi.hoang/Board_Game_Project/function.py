import pandas as pd
from scipy.stats import beta


def function_bayesian_average(row):
    m = row['rating_average']
    n = row['rating_number']
    bayesian_avg = (prior_mean * prior_weight + m * n) / (prior_weight + n)
    return bayesian_avg


# beta distribution function to calculate bayesian average
def calculate_bayesian_average(rating_sum, rating_number, prior_weight, prior_average):
    alpha = prior_weight + rating_sum
    beta_ = prior_weight + rating_number - rating_sum
    mean = beta.stats(alpha, beta_, moments='m')
    return mean





