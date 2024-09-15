import math
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np

from itertools import zip_longest
from operator import is_not
from functools import partial

def r(y):
    return y - math.floor(y)


def saw(y):
    return r(y) - (1/2)


# coor must be a list of length two corresponding to the coordinates of a point on the xy plane where 0 <= x,y < 1
def sawtooth(coor: list, k):
    #get rid of saw for x
    x = coor[0] + k*saw(coor[1])
    y = saw(coor[1] + coor[0] + k * saw(coor[1]))
    return [x, y]

#### Commented out code is an old version that is no longer in use.

# get the points for each coordinate
# def get_points(coor, n, k):
#     iter = 0
#     pts = []
#     temp_coor = coor.copy()
#     # do I have to add the original coordinates into the points to plot on the graph?
#     while iter < n:
#         temp_coor = sawtooth(temp_coor, k)
#         pts.append(temp_coor.copy())
#         iter+=1
#     return pts

# get the points and build a plot
# def build_plot(n, k):
#     coor = [-0.5, -0.5]
#     sample_pts = []
#     x = -0.5
#     y = -0.5
#     while x <= 0.5:
#         y = -0.5
#         while y <= 0.5:
#             sample_pts = get_points([x, y], n, k)
#             #print("y: ",  y)
#             res = list(zip(*sample_pts))
#             plt.plot(res[0], alpha=0.2)
#             y = y + 0.02
#         #print("x: ", x)
#         x = x +0.02
#     print(sample_pts)
#
#     #plt.axis('equal')
#     plt.show()
#

# get the sampled points for each period
# def get_period_points(coor, k, period, minmax):
#     iter = 0
#     pts = []
#     temp_coor = coor.copy()
#     # do I have to add the original coordinates into the points to plot on the graph?
#     while iter < (period + minmax[1]):
#         temp_coor = sawtooth(temp_coor, k)
#         if minmax[0] <= iter-period <= minmax[1]:
#             pts.append(temp_coor.copy())
#         iter+=1
#     return pts


# get which period the points are from
# def get_period_x(coor, k, period, minmax):
#     iter = 0
#     x = []
#     temp_coor = coor.copy()
#     # do I have to add the original coordinates into the points to plot on the graph?
#     while iter < (period + minmax[1]):
#         temp_coor = sawtooth(temp_coor, k)
#         if minmax[0] <= iter-period <= minmax[1]:
#             x.append(temp_coor[0])
#         iter+=1
#     return mean(x)

# get the points you would like to sample
# def get_period(k, period, minmax):
#     coor = [-0.5, -0.5]
#     sample_pts = []
#     x = -0.5
#     y = -0.5
#     avg = []
#     while x <= 0.5:
#         y = -0.5
#         while y <= 0.5:
#             temp = get_period_x([x, y], k, period, minmax)
#
#             avg.append(temp / math.sqrt(period))
#
#
#             y = y + 0.01
#
#         x = x +0.01
#
#     return avg



# get points and plot a histogram
# def plot_hist(k, increment, minmax, cap):
#     period = increment
#     res = []
#     while period <= cap:
#         res.append(get_period(k, period, minmax))
#         period = period + increment
#     for i in res:
#         plt.hist(i, bins=31, alpha = 0.2, label=cap)
#     plt.show()



# Returns a list of averages
# Each average is the average for each period
# Runs through all the periods in one go and returns a list of averages for each period
# Have to call this multiple times in a loop. one call for one coordinate.
def get_avgs(coor, k, periods: list, minmax, cap):
    iter = 0
    x = []
    temp_coor = coor.copy()
    avgs = []
    curr_period = 0
    while iter < cap + minmax[1]:
        temp_coor = sawtooth(temp_coor, k)
        if minmax[0] <= iter-periods[curr_period] <= minmax[1]:
            x.append(temp_coor[0])
        iter+=1
            # if the length of x equals the minmax period
        if len(x) == minmax[1] - minmax[0]:
            avgs.append(mean(x))
            curr_period += 1
            x = []
    return avgs


# Gets and sorts averages of the sampled points for each period.
# Averages are sorted based on periods to make histograms easier
def sort_avgs(k, period, minmax, increment, cap):
    # first create the periods list to be sent in
    periods = []
    temp_period = period
    while temp_period <= cap:
        periods.append(temp_period)
        temp_period = temp_period + increment

    ls_of_avgs = []

    x = -0.5
    while x <= 0.5:
        y = -0.5
        while y <= 0.5:
            temp = get_avgs([x, y], k, periods, minmax, cap)
            print(temp)
            ratios = []
            for t, p in zip(temp, periods):
                if abs(t) > 1:
                    ratios.append(t/math.sqrt(p))
                else:
                    ratios.append(None)


            if ratios != []:
                ls_of_avgs.append(ratios)

            y = y + 0.05
        x = x +0.05
    ls_periods = list(zip(*ls_of_avgs))


    filter_period = [[x for x in l if x is not None] for l in ls_periods]
    print(filter_period)
    return filter_period

# Create a histogram with the given requirements
#### NOTE: period is where you would like the begin your sampling, minmax is the range around each period you would like
# to sample, increment is how much you would like to increase by, and cap is the max value you would like to sample.
def create_hist(k, period, minmax, increment, cap):
    hists = sort_avgs(k, period,minmax, increment, cap)
    ls_bins = np.arange(-0.5, 0.5, (0.4/31.0))
    for his in hists:
        plt.hist(his, bins=ls_bins, alpha=0.2, label=cap)
    plt.show()


create_hist(-0.871, 10000, (-100, 100), 10000, 300000)


