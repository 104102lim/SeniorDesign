"""
Testing program for the Plotting module for the GUI
Xiangxing Liu
09/16/2018
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def test():
    print("test main funtion")
    x = np.linspace(-1, 1, 50)
    y1 = 2 * x + 1
    y2 = x**2
    color = 'red'
    linewidth = 1.0
    linestyle = '--'
    xlabel = 'I am x'
    ylabel = 'I am y'
    plot(x, y2, color, linewidth, linestyle, xlabel, ylabel)


def plot(x, y, color, linewidth, linestyle, xlabel, ylabel):
    plt.plot(x, y, color, linewidth, linestyle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


if __name__ == '__main__':
    test()
