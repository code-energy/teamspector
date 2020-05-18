# Functions for calculating aggregation values from a set of data.

import numpy as np


__all__ = ['maximum', 'minimum', 'median', 'mean', 'std_dev']


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
