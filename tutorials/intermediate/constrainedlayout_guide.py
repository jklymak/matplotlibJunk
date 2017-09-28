"""
================================
Constrained Layout Guide
================================

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

# sphinx_gallery_thumbnail_number = 18

#import matplotlib
#matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

import matplotlib.layoutbox as layoutbox

plt.rcParams['savefig.facecolor'] = "0.8"
plt.rcParams['figure.figsize'] = 4.5, 4.


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


fig, ax = plt.subplots()
example_plot(ax, fontsize=24)

###############################################################################
# To prevent this, the location of axes needs to be adjusted. For
# subplots, this can be done by adjusting the subplot params
# (:ref:`howto-subplots-adjust`). However, specifying your figure with the
# ``constrained_layout=True`` kwarg will do the adjusting automatically.

fig, ax = plt.subplots(constrained_layout=True)
example_plot(ax, fontsize=24)

###############################################################################
# When you have multiple subplots, often you see labels of different
# axes overlapping each other.

fig, axs = plt.subplots(2, 2, constrained_layout=False)
for ax in axs.flatten():
    example_plot(ax)

###############################################################################
# Specifying `constrained_layout=True` in the call to `plt.subplots`
# causes the layout to be properly constrained.

fig, axs = plt.subplots(2, 2, constrained_layout=True)
for ax in axs.flatten():
    example_plot(ax)

###############################################################################
# Colorbars
# =========
#
# If you create a colorbar with the :func:`~matplotlib.pyplot.colorbar`
# command you need to make room for it.  ``constrained_layout`` does this
# automatically.  Note that if you specify ``use_gridspec=True`` it will be
# ignored because this option is made for improving the layout via
# ``tight_layout``.

arr = np.arange(100).reshape((10, 10))
fig, ax = plt.subplots(figsize=(4, 4), constrained_layout=True)
im = ax.pcolormesh(arr, rasterized=True)
fig.colorbar(im, ax=ax, shrink=0.6)

############################################################################
# If you specify multiple axes to the ``ax`` argument of ``colorbar``,
# constrained_layout will take space from all axes that share the same
# gridspec.

fig, axs = plt.subplots(2, 2, figsize=(4, 4), constrained_layout=True)
for ax in axs.flatten():
    im = ax.pcolormesh(arr, rasterized=True)
fig.colorbar(im, ax=axs, shrink=0.6)

####################################################
# Suptitle
# =========
#
# ``constrained_layout`` can also make room for ``suptitle``.

fig, axs = plt.subplots(2, 2, figsize=(4, 4), constrained_layout=True)
for ax in axs.flatten():
    im = ax.pcolormesh(arr, rasterized=True)
fig.colorbar(im, ax=axs, shrink=0.6)
fig.suptitle('Big Suptitle')

####################################################
# Legends
# =======
#
# Legends can be placed outside
# of their parent axis.  Constrained-layout is designed to handle this.
# However, constrained-layout does *not* handle legends being created via
# ``fig.legend()`` (yet).


fig, ax = plt.subplots(constrained_layout=True)
ax.plot(np.arange(10), label='This is a plot')
ax.legend(loc='center left', bbox_to_anchor=(0.9, 0.5))

plt.show()

#############################################
# However, this will steal space from a subplot layout:

fig, axs = plt.subplots(2, 2, constrained_layout=True)
for ax in axs.flatten()[:-1]:
    ax.plot(np.arange(10))
axs[1, 1].plot(np.arange(10), label='This is a plot')
axs[1, 1].legend(loc='center left', bbox_to_anchor=(0.9, 0.5))

###############################################################################
# Padding and Spacing
# ===================
#
# For constrained_layout, we have implimented a padding around the edge of
# each axes.  This padding sets the distance from the edge of the plot,
# and the minimum distance between adjacent plots.  It is specified in
# inches by the keyword arguments `w_pad` and `h_pad` to the function
# `fig.set_constrained_layout_pads`:

fig, axs = plt.subplots(2, 2, constrained_layout=True)
for ax in axs.flatten():
    example_plot(ax, nodec=True)
    ax.set_xticklabels('')
    ax.set_yticklabels('')
fig.set_constrained_layout_pads(w_pad=4./72., h_pad=4./72.,
        hspace=0., wspace=0.)

fig, axs = plt.subplots(2, 2, constrained_layout=True)
for ax in axs.flatten():
    example_plot(ax, nodec=True)
    ax.set_xticklabels('')
    ax.set_yticklabels('')
fig.set_constrained_layout_pads(w_pad=2./72., h_pad=2./72.,
        hspace=0., wspace=0.)

##########################################
# Spacing between subplots is set by `wspace` and `hspace`.  There are
# specified as a fraction of the size of the subplot group as a whole.
# If the size of the figure is changed, then these spaces change in
# proportion.  Note in the blow how the space at the edges doesn't change from
# the above, but the space between subplots does.

fig, axs = plt.subplots(2, 2, constrained_layout=True)
for ax in axs.flatten():
    example_plot(ax, nodec=True)
    ax.set_xticklabels('')
    ax.set_yticklabels('')
fig.set_constrained_layout_pads(w_pad=2./72., h_pad=2./72.,
        hspace=0.2, wspace=0.2)


##########################################
# Spacing with colorbars
# -----------------------
#
# Colorbars still respect the `w_pad` and `h_pad` values.  However they will
# be `wspace` and `hsapce` apart from other subplots.  Note the use of a `pad`
# kwarg here in the `colorbar` call.  It defaults to 0.02 of the size of the
# axis it is attached to.

fig, axs = plt.subplots(2, 2, constrained_layout=True)
for ax in axs.flatten():
    pc = ax.pcolormesh(arr, rasterized=True)
    fig.colorbar(im, ax=ax, shrink=0.6, pad=0)
    ax.set_xticklabels('')
    ax.set_yticklabels('')
fig.set_constrained_layout_pads(w_pad=2./72., h_pad=2./72.,
        hspace=0.2, wspace=0.2)

##########################################
# In the above example, the colorbar will not ever be closer than 2 pts to
# the plot, but if we want it a bit further away, we can specify its value
# for `pad` to be non-zero.

fig, axs = plt.subplots(2, 2, constrained_layout=True)
for ax in axs.flatten():
    pc = ax.pcolormesh(arr, rasterized=True)
    fig.colorbar(im, ax=ax, shrink=0.6, pad=0.05)
    ax.set_xticklabels('')
    ax.set_yticklabels('')
fig.set_constrained_layout_pads(w_pad=2./72., h_pad=2./72.,
        hspace=0.2, wspace=0.2)



##########################################
# rcParams:
# -----------
#
# There are four `rcParams` that can be set, either in a script
# or in the `matplotlibrc` file.  They all have the prefix
# `figure.constrainedlayout`:
#
#  - `do`: Whether to do constrained_layout. Default is False
#  - `w_pad`, `h_pad`    Padding around axes objects.  Float representing inches.  Default is 3./72. inches (3 pts)
#  - `wspace`, `hspace`  Space between subplot groups.  Float representing a fraction of the suplot widths being separated.  Default is 0.02.

plt.rcParams['figure.constrainedlayout.do'] = True
fig, axs = plt.subplots(2, 2, figsize=(3, 3))
for ax in axs.flatten():
    example_plot(ax)

#############################
# Use with GridSpec
# =================
#
# constrained_layout is meant to be used
# with :func:`~matplotlib.figure.Figure.subplots` or
# :func:`~matplotlib.gridspec.GridSpec` and
# :func:`~matplotlib.figure.Figure.add_subplot`.

fig = plt.figure(constrained_layout=True)

gs1 = gridspec.GridSpec(2, 1, fig=fig)
ax1 = fig.add_subplot(gs1[0])
ax2 = fig.add_subplot(gs1[1])

example_plot(ax1)
example_plot(ax2)

###############################################################################
# More complicated gridspec layouts are possible...

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

############################################################################
# Note that in the above the left and columns don't have the same vertical
# extent.  If we want the top and bottom of the two grids to line up then
# they need to be in the same gridspec:

fig = plt.figure(constrained_layout=True)

gs0 = gridspec.GridSpec(6, 2, fig=fig)

ax1 = fig.add_subplot(gs0[:3, 0])
ax2 = fig.add_subplot(gs0[3:, 0])

example_plot(ax1)
example_plot(ax2)

ax = fig.add_subplot(gs0[0:2, 1])
example_plot(ax)
ax = fig.add_subplot(gs0[2:4, 1])
example_plot(ax)
ax = fig.add_subplot(gs0[4:, 1])
example_plot(ax)

############################################################################
# This example uses two gridspecs to have the colorbar only pertain to
# one set of pcolors.  Note how the left column is wider than the
# two right-hand columns because of this.  Of course, if you wanted the
# subplots to be the same size you only needed one gridspec.


def docomplicated(suptitle=None):
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
    fig.colorbar(pcm, ax=axs)
    if suptitle is not None:
        fig.suptitle(suptitle)

docomplicated()

###############################################################################
# Limitations
# ========================
#
# Incompatible functions
# ----------------------
#
# ``constrained_layout`` will not work on subplots
# created via the `subplot` command.  The reason is that each of these
# commands creates a separate `GridSpec` instance and `constrained_layout`
# uses (nested) gridspecs to carry out the layout.  So the following fails
# to yield a nice layout:


fig = plt.figure(constrained_layout=True)

ax1 = plt.subplot(221)
ax2 = plt.subplot(223)
ax3 = plt.subplot(122)

example_plot(ax1)
example_plot(ax2)
example_plot(ax3)

###############################################################################
# Of course that layout is possible using a gridspec:

fig = plt.figure(constrained_layout=True)
gs = gridspec.GridSpec(2, 2, fig=fig)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[:, 1])

example_plot(ax1)
example_plot(ax2)
example_plot(ax3)

###############################################################################
# Similarly,
# :func:`~matplotlib.pyplot.subplot2grid` doesn't work for the same reason:
# each call creates a different parent gridspec.

fig = plt.figure(constrained_layout=True)

ax1 = plt.subplot2grid((3, 3), (0, 0))
ax2 = plt.subplot2grid((3, 3), (0, 1), colspan=2)
ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=2)
ax4 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)

example_plot(ax1)
example_plot(ax2)
example_plot(ax3)
example_plot(ax4)

###############################################################################
# The way to make this plot compatible with ``constrained_layout`` is again
# to use ``gridspec`` directly

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

###############################################################################
# Caveats
# --------
#
#  * ``constrained_layout`` only considers ticklabels,
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
#    :func:`~matplotlib.pyplot.subplot2grid` don't work.  ``tight_layout``
#    *does* work with those functions, but doesn't work with nested
#    ``gridspec`` constructs.
#

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

fig, axs = plt.subplots(2, 6, figsize=(2, 2), constrained_layout=True)
for ax in axs.flatten():
    ax.plot(np.arange(10))

###################################################################
# This is easily fixed by making the figure large enough.
#
# If there is a bug, please report with a self-contained example that does
# not require outside data or dependencies (other than perhaps numpy).
