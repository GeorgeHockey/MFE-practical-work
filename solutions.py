"""
This is a mock of the format that is expected for the
autograder. The autograder will import this file and
then run the function. Your file should import anything
that is needed to run.

Your file can have any legal python file name. For example

assignment2.py
my_solutions.py
mfe_computational_assignment.py
autograder.py

are all reasonable names.

It should not have your actual name in it anywhere.

The functions names must match **exactly** including _ and capitalization.
Input variable names should also match, so that the autograder could
call

summary_statistics(returns=x)

or just

summary_statistics(x)
"""

# Any imports your code needs must be imported in your solutions file
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


# The funny returns: Series is how we can tell smart editors like PyCharm
# or VS Code that returns is a pandas Series. These editors can then help
# us to autocomplete available methods. This is optional, and
# def summary_statistics(prices):
# will work just as well
def summary_statistics(prices: Series):
    """
    Computes summary statistics

    Parameters
    ----------
    prices : Series
        Series containing daily prices of an index or portfolio

    Returns
    -------
    stats : DataFrame
        A DataFrame containing mean, standard deviation, skewness
        and kurtosis for returns sampled daily, weekly, monthly
        and quarterly
    """
    # Your code goes here.
    # Be sure to replace stats with the correct code
    stats = pd.DataFrame(columns= ["Daily","Weekly","Monthly","Quarterly"],
                         index=["mean","std","skew","kurt"])

    return stats


def students_dof(std_returns: Series):
    """
    Computes two measures of the DoF from a Student's t

    Parameters
    ----------
    std_returns : Series
        Series containing returns standardized to have mean 0 and variance 1

    Returns
    -------
    mle : float
        MLE estimate of the degree-of-freedom parameter
    moment : float
        Kurtosis-based estimate of the degree-of-freedom parameter
    """
    # Your code goes here.
    # Be sure to replace mle and moment with the correct code
    mle = 0.0
    moment = 0.0

    return mle, moment
