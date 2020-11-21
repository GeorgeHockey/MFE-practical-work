#!/usr/bin/env python
# coding: utf-8

# # Demo Autograder
# 
# This file can be run against your code to understand the basics of how the autograder works.  The autograder:
# 
# * loads your file as a Python module
# * runs each function
# * checks the output of each function
# 
# The formal tests are not included. The tests included in this file are sanity checks.
# 
# To run this on your code, please the notebook in the same folder as your `.py` file. Then set `FILENAME` to the name of your file.  You should then be able to run it.  If you see an `AssertionError` then your code isn't passing a sanity check.

# In[1]:


from importlib.machinery import SourceFileLoader
import pandas as pd
import os
import glob
import pandas as pd
import numpy as np

ROOT = os.getcwd()
FILENAME = "PW_2_function_1.py"
FILE = os.path.join(ROOT, FILENAME)
mod = SourceFileLoader(FILENAME.split(".py")[0], FILE).load_module()


# In[2]:


rg = np.random.default_rng(38218301830131)
index = pd.bdate_range("2020-01-01", periods=10000, freq="D")
scale = np.sqrt(0.2 ** 2 / 252)
simulated_price = pd.Series(
    np.exp(scale * np.cumsum(rg.standard_normal(10000))), index=index
)

output = mod.summary_statistics(simulated_price)
assert isinstance(output, pd.DataFrame)
assert list(output.index) == ["mean", "std", "skew", "kurt"]
assert list(output.columns) == ["Daily", "Weekly", "Monthly", "Quarterly"]


# In[3]:


returns = simulated_price.pct_change().dropna()
mle, mom = mod.students_dof(returns)

assert isinstance(mle, float)
assert isinstance(mom, float)

