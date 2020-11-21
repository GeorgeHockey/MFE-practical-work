#!/usr/bin/env python
# coding: utf-8

# First function in MFE Practical Work 2 assignment
# 
# Designed to take a daily price pandas series
# 
# Returns a pandas dataframe of mean, std_dev, skew, kurt: 
# 
# Sampled from daily, weekly, monthly and annual data

# Points
# 
#  - Mean has small differences due to sampling mechanics
# 
#  - standard deviation differs slightly - most likely due to macro movements
# 
#  - need to check equations and scaling for skew and kurtosis
# 
#  - additionally check that we are resampling the returns data correctly

# In[44]:


import numpy as np
import pandas as pd

def summary_statistics(prices):

    d_returns = prices.pct_change().dropna()
    w_returns = prices.resample("W-FRI").last().pct_change().dropna()
    m_returns = prices.resample("M").last().pct_change().dropna()
    q_returns = prices.resample("Q").last().pct_change().dropna()
    # Convert prices to returns

    # Enclosed function to find mean, std, skew and kurt: gives annualised stats
    def process(returns, n):
        returns_mu = returns.mean()                         # mean returns per time period
        annual_mu = ((1 + returns_mu) ** n) -1                          # annualised mean returns

        returns_err = returns - returns_mu       
        returns_var = (returns_err ** 2).mean()             # average squared return ( 2nd moment)
        annual_var = returns_var * n                        # annual rescaled variance
        annual_std = np.sqrt(annual_var)                    # annual rescaled std deviation

        returns_mom3 = (returns_err ** 3).mean()
        returns_mom4 = (returns_err ** 4).mean()            # Third and Fourth moments


        annual_skew = (returns_mom3 / returns_var ** (3/2)) #/ np.sqrt(n)  # rescaled Skew and Kurtosis
        annual_kurt = (returns_mom4 / returns_var ** (4/2)) #/ n

        returns_stats = pd.Series([annual_mu, annual_std, annual_skew, annual_kurt], index = ["mean", "std", "skew", "kurt"])
        
        return returns_stats
         
    # Feed in daily, weekly, monthly and quarterly data
    d_stats = process(d_returns, n = 252).rename("Daily")
    w_stats = process(w_returns, n = 52 ).rename("Weekly")
    m_stats = process(m_returns, n = 12 ).rename("Monthly")
    q_stats = process(q_returns, n = 4  ).rename("Quarterly")

    # Concatenate the series into a dataframe
    stats = pd.concat([d_stats, w_stats, m_stats, q_stats], axis=1)

    return stats

# In[57]:

from scipy.special import gammaln
from scipy.optimize import minimize

def students_dof(cheese):
    def std_t_loglik(nu, x):
        # These are fixed for now
        mu = 0
        sigma2 = 1
        sigma = np.sqrt(sigma2)


        a = gammaln((nu + 1) / 2)
        b = gammaln(nu / 2)
        c = np.sqrt(np.pi * (nu-2))
        d = ((nu + 1) / 2)
        e = (x - mu) **2
        f = sigma2 * (nu - 2)

        loglik = a - b - np.log(c) - np.log(sigma) - d * np.log(1 + e / f)
        return -(loglik.sum())
    def calc_kurt(series):
        mu = series.mean()
        err = series - mu
        var = (err**2).mean()
        mom4 = (err**4).mean()
        kurt = mom4 / var ** (4/2)
        return kurt
    starting_val = np.array([3]) 
    opt = minimize(std_t_loglik, starting_val, args=(cheese), bounds=[(2.01, 100)], options={"disp": True})
    mle = opt.x[0]
    if calc_kurt(cheese) > 4:
        moment = 3*(((calc_kurt(cheese) - 2) / (calc_kurt(cheese) - 4)))
    else:
        moment = float('inf')
    return mle, moment

# %%