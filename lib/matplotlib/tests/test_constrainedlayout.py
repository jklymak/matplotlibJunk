from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six
import warnings

import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredOffsetbox, DrawingArea
from matplotlib.patches import Rectangle
import matplotlib.gridspec as gridspec
from matplotlib import ticker


def example_plot(ax, fontsize=12):
    ax.plot([1, 2])
    ax.locator_params(nbins=3)
    ax.set_xlabel('x-label', fontsize=fontsize)
    ax.set_ylabel('y-label', fontsize=fontsize)
    ax.set_title('Title', fontsize=fontsize)

def example_pcolor(ax, fontsize=12):
    dx, dy = 0.6, 0.6
    y, x = np.mgrid[slice(-3, 3 + dy, dy),
                    slice(-3, 3 + dx, dx)]
    z = (1 - x / 2. + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)
    pcm = ax.pcolormesh(x, y, z, cmap='RdBu_r', vmin=-1., vmax=1.,
                        rasterized=True)
    # ax.locator_params(nbins=3)
    ax.set_xlabel('x-label', fontsize=fontsize)
    ax.set_ylabel('y-label', fontsize=fontsize)
    ax.set_title('Title', fontsize=fontsize)
    return pcm

@image_comparison(baseline_images=['constrained_layout1'])
def test_constrained_layout1():
    'Test constrained_layout for a single subplot'
    fig = plt.figure(constrained_layout=True)
    ax = fig.add_subplot(111)
    example_plot(ax, fontsize=24)

@image_comparison(baseline_images=['constrained_layout2'])
def test_constrained_layout2():
    'Test constrained_layout for 2x2 subplots'
    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    #ax = fig.add_subplot(111)
    for ax in axs.flatten():
        example_plot(ax, fontsize=24)

@image_comparison(baseline_images=['constrained_layout3'])
def test_constrained_layout3():
    'Test constrained_layout for colorbars with subplots'
    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    #ax = fig.add_subplot(111)
    for ax in axs.flatten():
        pcm = example_pcolor(ax, fontsize=24)
        fig.colorbar(pcm, ax=ax, use_gridspec=False)

@image_comparison(baseline_images=['constrained_layout4'])
def test_constrained_layout4():
    'Test constrained_layout for a single colorbar with subplots'
    fig, axs = plt.subplots(2,2, constrained_layout=True)
    #ax = fig.add_subplot(111)
    for ax in axs.flatten():
        pcm = example_pcolor(ax, fontsize=24)
    fig.colorbar(pcm, ax=axs, use_gridspec=False, pad=0.01, shrink=0.6)

@image_comparison(baseline_images=['constrained_layout5'])
def test_constrained_layout5():
    'Test constrained_layout for a single colorbar with subplots, colorbar bottom'
    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    #ax = fig.add_subplot(111)
    for ax in axs.flatten():
        pcm = example_pcolor(ax, fontsize=24)
    fig.colorbar(pcm, ax=axs,
        use_gridspec=False, pad=0.01, shrink=0.6, location='bottom')

@image_comparison(baseline_images=['constrained_layout6'])
def test_constrained_layout6():
    'Test constrained_layout for nested gridspecs'
    fig = plt.figure(constrained_layout=True)
    gs = gridspec.GridSpec(1, 2, fig=fig)
    gsl = gridspec.GridSpecFromSubplotSpec(2, 2, gs[0])
    gsr = gridspec.GridSpecFromSubplotSpec(1, 2, gs[1])
    axsl = []
    for gs in gsl:
        ax = fig.add_subplot(gs)
        axsl += [ax]
        example_plot(ax, fontsize=12)
    ax.set_xlabel('x-label\nMultiLine')
    axsr = []
    for gs in gsr:
        ax = fig.add_subplot(gs)
        axsr += [ax]
        pcm = example_pcolor(ax, fontsize=12)

    fig.colorbar(pcm, ax = axsr, use_gridspec=False, pad=0.01, shrink=0.99, location='bottom', ticks=ticker.MaxNLocator(nbins=5))

@image_comparison(baseline_images=['constrained_layout8'])
def test_constrained_layout8():
    'Test for gridspecs that are not completely full'
    fig = plt.figure(figsize=(7,4), constrained_layout=True)
    gs = gridspec.GridSpec(3, 5, fig=fig)
    #ax = fig.add_subplot(111)
    axs = []
    j = 1
    for i in [0, 1]:
        ax = fig.add_subplot(gs[j, i])
        axs += [ax]
        pcm = example_pcolor(ax, fontsize=10)
        if i > 0:
            ax.set_ylabel('')
        if j < 1:
            ax.set_xlabel('')
        #axs[j, i].set_title('%d %d'%(j,i))
        ax.set_title('')
    j = 0
    for i in [2, 4]:
        ax = fig.add_subplot(gs[j, i])
        axs += [ax]
        pcm = example_pcolor(ax, fontsize=10)
        if i > 0:
            ax.set_ylabel('')
        if j < 1:
            ax.set_xlabel('')
        #axs[j, i].set_title('%d %d'%(j,i))
        ax.set_title('')
    ax = fig.add_subplot(gs[2,:])
    axs += [ax]
    pcm = example_pcolor(ax, fontsize=10)


    fig.colorbar(pcm, ax=axs, use_gridspec=False, pad=0.01, shrink=0.6)


@image_comparison(baseline_images=['constrained_layout7'])
def test_constrained_layout7():
    'Test for proper warning if fig not set in GridSpec'
    fig = plt.figure(tight_layout=True)
    gs = gridspec.GridSpec(1, 2)
    gsl = gridspec.GridSpecFromSubplotSpec(2, 2, gs[0])
    gsr = gridspec.GridSpecFromSubplotSpec(1, 2, gs[1])
    axsl = []
    for gs in gsl:
        ax = fig.add_subplot(gs)
        axsl += [ax]
        example_plot(ax, fontsize=12)
    ax.set_xlabel('x-label\nMultiLine')
    axsr = []
    for gs in gsr:
        ax = fig.add_subplot(gs)
        axsr += [ax]
        pcm = example_pcolor(ax, fontsize=12)

    fig.colorbar(pcm, ax = axsr, use_gridspec=False, pad=0.01,
                shrink=0.99, location='bottom',
                ticks=ticker.MaxNLocator(nbins=5))

@image_comparison(baseline_images=['constrained_layout8'],
        extensions=['png', 'pdf'])
def test_constrained_layout8():
    'Test for gridspecs that are not completely full'
    fig = plt.figure(figsize=(10,5), constrained_layout=True)
    gs = gridspec.GridSpec(3, 4, fig=fig)
    #ax = fig.add_subplot(111)
    axs = []
    j = 1
    for i in [0, 3]:
        ax = fig.add_subplot(gs[j, i])
        axs += [ax]
        pcm = example_pcolor(ax, fontsize=9)
        if i > 0:
            ax.set_ylabel('')
        if j < 1:
            ax.set_xlabel('')
        #axs[j, i].set_title('%d %d'%(j,i))
        ax.set_title('')
    j = 0
    for i in [1]:
        ax = fig.add_subplot(gs[j, i])
        axs += [ax]
        pcm = example_pcolor(ax, fontsize=9)
        if i > 0:
            ax.set_ylabel('')
        if j < 1:
            ax.set_xlabel('')
        #axs[j, i].set_title('%d %d'%(j,i))
        ax.set_title('')
    ax = fig.add_subplot(gs[2,:])
    axs += [ax]
    pcm = example_pcolor(ax, fontsize=9)


    fig.colorbar(pcm, ax=axs, use_gridspec=False, pad=0.01, shrink=0.6)
