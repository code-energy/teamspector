# Functions for calculating aggregation values from a set of data.

import numpy as np

# XXX: Do not import any functions to this name space without a leading `_`
# character, or else the experiment runner will try to import and run the
# function to aggregate data.


def maximum(data):
    return max(data)


def minimum(data):
    return min(data)


def median(data):
    return np.median(data)


def mean(data):
    return np.mean(data)


def std_dev(data):
    return np.std(data)
