"""
===============================
Specifying Ticks and Ticklabels
===============================

Axis ticks can be specified in a number of ways in Matplotlib.  Laregly the
automatic tick locators and formatters are adequate, but this guide is
for further customization.

Further information can be found in the `.Axes` and `.ticker` documentation.
"""

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

mpl.rcParams['figure.constrained_layout.use'] = True
mpl.rcParams['figure.figsize'] = 6.4, 3.5

############################################################################
# Directly specifying ticks and labels
# ====================================
#
# Often its fine to specify the ticks and/or ticklabels directly using
# `.Axes.set_xticks`, `.Axes.set_yticks` for the tick values and
# `.Axes.set_xticklabels` and `.Axes.set_yticklabels` for the tick labels.

fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.5))
axs[0].plot(np.arange(10))
axs[0].set_xlabel('Auto x-ticks')

axs[1].plot(np.arange(10))
axs[1].set_xticks([0., 5., 7., 10.])
axs[1].set_xlabel('Manual x-ticks')

axs[2].plot(np.arange(10))
axs[2].set_xticks([0., 5., 7., 10.])
axs[2].set_xticklabels(['Start', 'Mid', 'Boo', 'End'])
axs[2].set_xlabel('Manual x-ticks and labels')
plt.show()
