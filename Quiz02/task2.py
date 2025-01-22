from scipy import stats

import numpy as np
from numpy import random as rd
import statistics as st
import matplotlib.pyplot as plt

def generate_array(size = 600, mean=170, std_dev=10):
    """
    Create a 1D array filled with 600 random integers in the range [0, 100] (use the
    np.random.randint function).
    :param size: number of elements in the array
    :param mean (float): mean of the nomral distribution, by default 170
    :param std_dev (float): standard deviation of the normal distribution, by default 10
    :return: array as a list filled with random integers in the range [0, 100]
    """
    array = np.random.randint(100)
    return array

def descriptive_statistics(array_data):
    """
     Calculate both the mean AND the standard deviation of all elements in the array.

    :param array_data (list): a list of random values
    :return tuple: tuple with the mean and standard deviation of array
    """
    mean = st.mean(array_data)
    std_dev = st.stdev(array_data)
    return round(mean,2), round(std_dev,2)

def extrema_values(array_data):
    """
    Looking for the index of the maximum value in the array

    :param array_data (list): a list of random values
    :return index_max_value which is a index og maximum value
    """
    max_value = np.max(array_data)
    index_max_value = np.where(array_data == max_value)

    return index_max_value

def add_20_percent(array_data):
    """
    Adds 20% to every element in the array.
    :param array_data: a list of randomized values in range of [0,100]
    :return: array_data with each element increased by 20%
    """
    increased_array_data = array_data*1.20
    return increased_array_data

def boxplot(increased_array_data):
    """
    Graphical representation of the data in a form of a box plot

    :param array_data: a list of randomized values in range of [0,100]
    :return: boxplot
    """
    arrays = increased_array_data

    box = plt.boxplot(arrays, patch_artist=True,
                      boxprops=dict(facecolor="powderblue", color="lightsteelblue"),
                      flierprops=dict(markerfacecolor="lightsteelblue", marker="o"),
                      medianprops=dict(color="lightsteelblue"))

    plt.title("(original array)-(increased array)", fontsize=12)
    plt.xlabel("status", fontsize=12)
    plt.ylabel("distribution", fontsize=12)
    plt.xticks([1, 2], ["original array", "increased array"])
    plt.show()

def information():
    """ Prints all caluclated infroms"""
    print(generate_array())
    print(descriptive_statistics())
    print(extrema_values())
    print(add_20_percent())
    print(boxplot())
