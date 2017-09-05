"""
==================
Constrained Layout guide
==================

How to use constrained-layout to fit plots within your figure cleanly.

*constrained_layout* automatically adjusts subplots and decorations like
legends and colorbars so that they fit in the figure window wihile still
preserving, as best they can, the logical layout requested by the user.

*constrained_layout* is similar to *tight_layout*, but uses a constraint
solver to determine the size of axes that allows them to fit.

Simple Example
==============

In matplotlib, the location of axes (including subplots) are specified in
normalized figure coordinates. It can happen that your axis labels or
titles (or sometimes even ticklabels) go outside the figure area, and are thus
clipped.

"""

import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.layoutbox as layoutbox

plt.rcParams['savefig.facecolor'] = "0.8"


def example_plot(ax, fontsize=12, nodec=False):
    ax.plot([1, 2])

    ax.locator_params(nbins=3)
    if not nodec:
        ax.set_xlabel('x-label', fontsize=fontsize)
        ax.set_ylabel('y-label', fontsize=fontsize)
        ax.set_title('Title', fontsize=fontsize)
    else:
        ax.set_xticklabels('')
        ax.set_yticklabels('')


def show():
    #pass
    plt.show()

plt.close('all')
fig, ax = plt.subplots()
example_plot(ax, fontsize=24)

###############################################################################
# To prevent this, the location of axes needs to be adjusted. For
# subplots, this can be done by adjusting the subplot params
# (:ref:`howto-subplots-adjust`). Matplotlib v1.1 introduces a new
# command :func:`~matplotlib.pyplot.tight_layout` that does this
# automatically for you.

fig, ax = plt.subplots(constrained_layout=True)
example_plot(ax, fontsize=24)

###############################################################################
# When you have multiple subplots, often you see labels of different
# axes overlapping each other.

plt.close('all')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
example_plot(ax1)
example_plot(ax2)
example_plot(ax3)
example_plot(ax4)

show()
###############################################################################
# Specifying `constrained_layout=True` in the call to `plt.subplots`
# causes the layout to be properly constrained.

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2,
                                             constrained_layout=True)
example_plot(ax1)
example_plot(ax2)
example_plot(ax3)
example_plot(ax4)
show()
###############################################################################
# :func:`~matplotlib.figure.constrained_layout` can take keyword arguments of
# *pad*, *w_pad* and *h_pad*. These control the extra padding around the
# figure border and between subplots. The padding can be a float (figure-
# relative units), or a float followed by "pt" for points, "in" for inches,
# "mm", and "cm".

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
example_plot(ax1)
example_plot(ax2)
example_plot(ax3)
example_plot(ax4)
fig.constrained_layout(w_pad='24pt', h_pad='8pt')
show()
###############################################################################
# :func:`~matplotlib.figure.constrained_layout` will not work on subplots
# created via the `subplot` command.  The reason is that each of these
# commands creates a separate `GridSpec` instance and `constrained_layout`
# uses (nested) gridspecs to carry out the layout.  So the following fails
# to yield a nice layout:

plt.close('all')
fig = plt.figure(constrained_layout=True)

ax1 = plt.subplot(221)
ax2 = plt.subplot(223)
ax3 = plt.subplot(122)

example_plot(ax1)
example_plot(ax2)
example_plot(ax3)

show()

###############################################################################
# Of course that layout is possible using a gridspec:

# This one fails because there is nothing to enforce that the ax.layoutbox
# must fill the ss box....


import matplotlib.gridspec as gridspec

plt.close('all')
fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(2, 2, fig=fig)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[:, 1])

example_plot(ax1)
example_plot(ax2)
example_plot(ax3)

show()

###############################################################################
# Similarly,
# :func:`~matplotlib.pyplot.subplot2grid` doesn't work for the same reason:
# each call creates a differnt parent gridspec.

plt.close('all')
fig = plt.figure(constrained_layout=True)

ax1 = plt.subplot2grid((3, 3), (0, 0))
ax2 = plt.subplot2grid((3, 3), (0, 1), colspan=2)
ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=2)
ax4 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)

example_plot(ax1)
example_plot(ax2)
example_plot(ax3)
example_plot(ax4)

show()


###############################################################################
# The way to make this plot compatible with ``constrained_layout`` is again
# to use ``gridspec`` directly

plt.close('all')
fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(3, 3, fig=fig)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1:])
ax3 = fig.add_subplot(gs[1:, 0:2])
ax4 = fig.add_subplot(gs[1:, -1])

example_plot(ax1)
example_plot(ax2)
example_plot(ax3)
example_plot(ax4)

show()
plt.show()
layoutbox.print_tree(fig.layoutbox)
plt.show()

###############################################################################
# Caveats
# =======
#
#  * :func:`~matplotlib.figure.constrain_layout` only considers ticklabels,
#    axis labels, titles, and legends.  Thus, other artists may be clipped
#    and also may overlap.
#
#  * It assumes that the extra space needed for ticklabels, axis labels,
#    and titles is independent of original location of axes. This is
#    often true, but there are rare cases where it is not.
#
#  * As above, layouts are carried out in each "parent" gridspec
#    independently.  That means that some ``pyplot`` convenience wrappers
#    like :func:`~matplotlib.pyplot.subplot` and
#    :func:`~matplotlib.figure.subplot2grid` don't work.  ``tight_layout``
#    *does* work with those functions, but doesn't work with nested
#    ``gridspec`` constructs.
#
#
# Use with GridSpec
# =================
#
# As the examples above make clear, ``constrained_layout`` is meant to be used
# with :func:`~matplotlib.figure.subplots` or
# :func:`~matplotlib.gridspec.GridSpec` and
# :func:`~matplotlib.figure.add_subplot`.

plt.close('all')
fig = plt.figure(constrained_layout=True)

gs1 = gridspec.GridSpec(2, 1, fig=fig)
ax1 = fig.add_subplot(gs1[0])
ax2 = fig.add_subplot(gs1[1])

example_plot(ax1)
example_plot(ax2)

###############################################################################
# More complicated gridspec layouts are possible...
plt.close('all')

fig = plt.figure(constrained_layout=True)

gs0 = gridspec.GridSpec(1, 2, fig=fig)

gs1 = gridspec.GridSpecFromSubplotSpec(2, 1, gs0[0])
ax1 = fig.add_subplot(gs1[0])
ax2 = fig.add_subplot(gs1[1])

example_plot(ax1)
example_plot(ax2)

gs2 = gridspec.GridSpecFromSubplotSpec(3, 1, gs0[1])

for ss in gs2:
    ax = fig.add_subplot(ss)
    example_plot(ax)
    ax.set_title("")
    ax.set_xlabel("")

ax.set_xlabel("x-label", fontsize=12)
show()
# plt.show()

############################################################################
# If we want the top and bottom of the two grids to line up then they need
# to be in the same gridspec.
plt.close('all')

fig = plt.figure(constrained_layout=True)

gs0 = gridspec.GridSpec(6, 2, fig=fig)

ax1 = fig.add_subplot(gs0[:3, 1])
ax2 = fig.add_subplot(gs0[3:, 1])

example_plot(ax1)
example_plot(ax2)

ax = fig.add_subplot(gs0[0:2, 0])
example_plot(ax)
ax = fig.add_subplot(gs0[2:4, 0])
example_plot(ax)
ax = fig.add_subplot(gs0[4:, 0])
example_plot(ax)

show()


###############################################################################
# Colorbars
# =========
#
# If you create a colorbar with the :func:`~matplotlib.pyplot.colorbar`
# command you need to make room for it.  ``constrained_layout`` does not work
# with ``use_gridspec=True`` which is now the default so we explicitly
# set ``use_gridspec=False``.

plt.close('all')
arr = np.arange(100).reshape((10, 10))
fig = plt.figure(figsize=(4, 4), constrained_layout=True)
im = plt.imshow(arr, interpolation="none")
fig.colorbar(im, use_gridspec=False)
show()

############################################################################
# If you specify multiple axes to the ``ax`` argument of ``colorbar``,
# constrained_layout will take space from all axes that share the same
# gridspec.

plt.close('all')
arr = np.arange(100).reshape((10, 10))
fig, axs = plt.subplots(2, 2, figsize=(4, 4), constrained_layout=True)
for ax in axs.flatten():
    im = ax.imshow(arr, interpolation="none")
fig.colorbar(im, ax=axs, use_gridspec=False)
show()

############################################################################
# This example uses two gridspecs to have the colorbar only pertain to
# one set of pcolors.  Note how the left column is slightly wider than the
# two right-hand columns because of this.

plt.close('all')
fig = plt.figure(constrained_layout=True)
gs0 = gridspec.GridSpec(1, 2, fig=fig, width_ratios=[1., 2.])
gsl = gridspec.GridSpecFromSubplotSpec(2, 1, gs0[0])
gsr = gridspec.GridSpecFromSubplotSpec(2, 2, gs0[1])

for gs in gsl:
    ax = fig.add_subplot(gs)
    example_plot(ax)
axs = []
for gs in gsr:
    ax = fig.add_subplot(gs)
    pcm = ax.pcolormesh(arr, rasterized=True)
    ax.set_xlabel('x-label')
    ax.set_ylabel('y-label')
    ax.set_title('title')

    axs += [ax]
fig.colorbar(pcm, ax=axs, use_gridspec=False)
show()

####################################################
# Legends
# =======
#
# Legends can be placed outside
# of their parent axis.  Constrained-layout is designed to handle this.
# However, constrained-layout does *not* handle legends being created via
# ``fig.legend()``.

plt.close('all')
fig, ax = plt.subplots(constrained_layout=True)
ax.plot(np.arange(10), label='This is a plot')
ax.legend(loc='center left', bbox_to_anchor=(0.9, 0.5))
show()

#############################################
# However, this will steal space from a subplot layout:

plt.close('all')
fig, axs = plt.subplots(2, 2, constrained_layout=True)
for ax in axs.flatten()[:-1]:
    ax.plot(np.arange(10))
axs[1, 1].plot(np.arange(10), label='This is a plot')
axs[1, 1].legend(loc='center left', bbox_to_anchor=(0.9, 0.5))
show()

###########################################################
# Debugging
# =========
#
# Constrained-layout can fail in somewhat unexpected ways.  Because it uses
# a constraint solver the solver can find solutions that are mathematically
# correct, but that aren't at all what the user wants.  The usual failure
# mode is for all sizes to collapse to their smallest allowable value. If
# this happens, it is for one of two reasons:
#
#   1. There was not enough room for the elements you were requesting to draw
#   2. There is a bug - in which case open an issue at
#      https://github.com/matplotlib/matplotlib/issues.
#
# As an example of 1:

plt.close('all')
fig, axs = plt.subplots(2, 6, figsize=(2, 2), constrained_layout=True)
for ax in axs.flatten():
    ax.plot(np.arange(10))
show()

# This is easily fixed by making the figure large enough.
#
# If there is a bug, please report with a self-contained example that does
# not require outside data or dependencies (other than perhaps numpy).
