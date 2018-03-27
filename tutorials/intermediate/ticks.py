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
import matplotlib.gridspec as gridspec

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

############################################################################
# Specifying minor ticks and labels
# =================================
#
# We can also specify minor ticks.  We can do it manually, or automatically
# using a `.ticker.Locator`.  Here we show both the `AutoMinorLocator` and
# the `MultipleLocator`.

fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.5))
axs[0].plot(np.arange(10))
axs[0].xaxis.set_ticks(np.arange(0, 10, 1.25), minor=True)
axs[0].set_xlabel('Manual minor x-ticks')

minorLocator = mticker.AutoMinorLocator()

axs[1].plot(np.arange(10))
axs[1].xaxis.set_minor_locator(minorLocator)
axs[1].set_xlabel('Auto minor x-ticks')

multipleLocator = mticker.MultipleLocator(0.5)

axs[2].plot(np.arange(10))
axs[2].xaxis.set_minor_locator(multipleLocator)
axs[2].set_xlabel('Set Multiple x-ticks')

plt.show()

############################################################################
# Note that if we resize the Axes, the `.ticker.AutoMinorLocator`
# adjusts the number of minor ticks. Automatic
# locators are usually a better choice if the axes size is not known or
# likely to change.

fig = plt.figure(figsize=(6.4, 2.5))
gs = gridspec.GridSpec(1, 10, figure=fig)
ax = fig.add_subplot(gs[0])
ax.plot(np.arange(10))
minorLocator = mticker.AutoMinorLocator()
ax.xaxis.set_minor_locator(minorLocator)
ax.set_xlabel('Auto minor x-ticks')

ax = fig.add_subplot(gs[1:])
ax.plot(np.arange(10))
minorLocator = mticker.AutoMinorLocator()
ax.xaxis.set_minor_locator(minorLocator)
ax.set_xlabel('Auto minor x-ticks')
plt.show()

############################################################################
# Of course, an array of `.ticker.Locator` subclasses are also appropriate
# for the major ticks as well.

locators = [mticker.AutoLocator(), mticker.LogLocator(),
        mticker.NullLocator()]
label = ['Auto', 'Log', 'Null']
fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.5))
for n, locator in enumerate(locators):
    axs[n].plot(np.arange(1, 200))
    axs[n].xaxis.set_major_locator(locator)
    axs[n].set_xlabel(label[n])
fig.align_xlabels(axs)
plt.show()




############################################################################
# TODO:
#   x minor ticks
#   - Changing auto formatting...
#      - options...
#      - FuncFormatter...
#   - Change auto Locating...
#   - date formatting and locating
