conda install numpy#!/usr/bin/env python
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
#  - Kurtosis and skew much larger at smaller intervals: this seems too great
#  
#  - Larger numbers in general due to singe stock movements - FTSE 100 is smaller 

# In[254]:


import numpy as np
import pandas as pd

def summary_statistics(prices):

    # Convert prices to returns
    returns = prices.pct_change()

    # Resample returns, using .sum()
    #  *100 to give % values  
    d_returns = returns * 100
    w_returns = returns.resample("W-FRI").sum() * 100
    m_returns = returns.resample("M").sum() * 100
    q_returns = returns.resample("Q").sum() * 100

    # Enclosed function to find mean, std, skew and kurt: gives annualised stats
    def process(returns, n):
        returns_mu = returns.mean()                         # mean returns per time period
        annual_mu = returns_mu * n                          # annualised mean returns

        returns_err = returns - returns_mu       
        returns_var = (returns_err ** 2).mean()             # average squared return ( 2nd moment)
        annual_var = returns_var * n                        # annual rescaled variance
        annual_std = np.sqrt(annual_var)                    # annual rescaled std deviation

        returns_mom3 = (returns_err ** 3).mean()
        returns_mom4 = (returns_err ** 4).mean()            # Third and Fourth moments


        annual_skew = (returns_mom3 / returns_var ** (3/2)) * np.sqrt(n)  # rescaled Skew and Kurtosis
        annual_kurt = (returns_mom4 / returns_var ** (4/2)) * n

        returns_stats = pd.Series([annual_mu, annual_std, annual_skew, annual_kurt], index = ["mean", "std", "skew", "kurt"])
        
        return returns_stats
         
    # Feed in daily, weekly, monthly and quarterly data
    d_stats = process(d_returns, 252).rename("Daily")
    w_stats = process(w_returns, 52 ).rename("Weekly")
    m_stats = process(m_returns, 12 ).rename("Monthly")
    q_stats = process(q_returns, 4  ).rename("Quarterly")

    # Concatenate the series
    stats = pd.concat([d_stats, w_stats, m_stats, q_stats], axis=1,)

    return stats


# In[ ]:





# In[238]:


aapl = pd.read_csv("data/aapl.csv", parse_dates=True, index_col="Date")
aapl_close = aapl["Close"]

sbry_1 = pd.read_csv("data/SBRY_1Y.csv", parse_dates=True, index_col="Date")
sbry_1 = sbry_1["Close"]

sbry_10 = pd.read_csv("data/SBRY_10Y.csv", parse_dates=True, index_col="Date")
sbry_10 = sbry_10["Close"]

FTSE = pd.read_csv("data/^FTSE.csv", parse_dates=True, index_col="Date")
FTSE = FTSE["Close"]


# In[255]:


summary_statistics(aapl_close)


# In[256]:


summary_statistics(sbry_1)


# In[257]:


summary_statistics(sbry_10)


# In[258]:


summary_statistics(FTSE)

