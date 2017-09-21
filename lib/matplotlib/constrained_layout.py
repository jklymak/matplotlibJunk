"""
This module provides the routine to adjust subplot layouts so that there are
no overlapping axes or axes decorations.  All axes decorations are dealt with
(labels, ticks, titles, ticklabels) and some dependent artists are also dealt
with (colorbar, suptitle, legend).

Layout is done via :meth:`~matplotlib.gridspec`, with one constraint per
gridspec, so it is possible to have overlapping axes if the gridspecs
overlap (i.e. using :meth:`~matplotlib.gridspec.GridSpecFromSubplotSpec`).
Axes placed using ``figure.subplots()`` or ``figure.add_subplots()`` will
participate in the layout.  Axes manually placed via ``figure.add_axes()``
will not.

See Tutorial (TODO: link)

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from matplotlib.legend import Legend
import matplotlib.transforms as transforms
import numpy as np
import matplotlib.layoutbox as layoutbox
import warnings

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(message)s')


def get_axall_tightbbox(ax, renderer):
    '''
    Get the tight_bbox of the axis ax, and any dependent decorations, like
    a `Legend` instance.
    '''

    # main bbox of the axis....
    bbox = ax.get_tightbbox(renderer=renderer)
    # now add the possibility of the legend...
    for child in ax.get_children():
        if isinstance(child, Legend):
            bboxn = child._legend_box.get_window_extent(renderer)
            bbox = transforms.Bbox.union([bbox, bboxn])
        # add other children here....
    return bbox


def insamecolumn(ss0, ssc):
    nrows, ncols = ss0.get_gridspec().get_geometry()

    if ss0.num2 is None:
        ss0.num2 = ss0.num1
    rowNum0min, colNum0min = divmod(ss0.num1, ncols)
    rowNum0max, colNum0max = divmod(ss0.num2, ncols)
    if ssc.num2 is None:
        ssc.num2 = ssc.num1
    rowNumCmin, colNumCmin = divmod(ssc.num1, ncols)
    rowNumCmax, colNumCmax = divmod(ssc.num2, ncols)
    if colNum0min >= colNumCmin and colNum0min <= colNumCmax:
        return True
    if colNum0max >= colNumCmin and colNum0max <= colNumCmax:
        return True
    return False


def insamerow(ss0, ssc):
    nrows, ncols = ss0.get_gridspec().get_geometry()

    if ss0.num2 is None:
        ss0.num2 = ss0.num1
    rowNum0min, colNum0min = divmod(ss0.num1, ncols)
    rowNum0max, colNum0max = divmod(ss0.num2, ncols)
    if ssc.num2 is None:
        ssc.num2 = ssc.num1
    rowNumCmin, colNumCmin = divmod(ssc.num1, ncols)
    rowNumCmax, colNumCmax = divmod(ssc.num2, ncols)
    if rowNum0min >= rowNumCmin and rowNum0min <= rowNumCmax:
        return True
    if rowNum0max >= rowNumCmin and rowNum0max <= rowNumCmax:
        return True
    return False


######################################################
def do_constrained_layout(fig, renderer, h_pad, w_pad):

    """
    Do the constrained_layout.  Called at draw time in
     ``figure.constrained_layout()``

    Parameters:


    fig: Figure
      is the ``figure`` instance to do the layout in.

    renderer: Renderer
      the renderer to use.

     h_pad, v_pad : float
       are in figure-normalized units.

    """

    '''  Steps:

    1. get a list of unique gridspecs in this figure.  Each gridspec will be
    constrained separately.
    2. Check for gaps in the gridspecs.  i.e. if not every axes slot in the
    gridspec has been filled.  If empty, add a ghost axis that is made so
    that it cannot be seen (though visible=True).  This is needed to make
    a blank spot in the layout.
    3. Compare the tight_bbox of each axes to its `position`, and assume that
    the difference is the space needed by the elements around the edge of
    the axes (decorations) like the title, ticklabels, x-labels, etc.  This
    can include legends who overspill the axes boundaries.
    4. Constrain gridspec elements to line up:
        a) if colnum0 neq colnumC, the two subplotspecs are stacked next to
        each other, with the appropriate order.
        b) if colnum0 == columnC line up the left or right side of the
        poslayoutbox (depending if it is the min or max num that is equal).
        c) do the same for rows...
    5. The above doesn't constrain relative sizes of the poslayoutboxes at
    all, and indeed zero-size is a solution that the solver often finds more
    convenient than expanding the sizes.  Right now the solution is to compare
    subplotspec sizes (i.e. drowsC and drows0) and constrain the larger
    poslayoutbox to be larger than the ratio of the sizes.  i.e. if drows0 >
    drowsC,  then ax.poslayoutbox > axc.poslayoutbox * drowsC / drows0. This
    works fine *if* the decorations are similar between the axes.  If the
    larger subplotspec has much larger axes decorations, then the constraint
    above is incorrect.

    We need the greater than in the above, in general, rather than an equals
    sign.  Consider the case of the left column having 2 rows, and the right
    column having 1 row.  We want the top and bottom of the poslayoutboxes to
    line up. So that means if there are decorations on the left column axes
    they will be smaller than half as large as the right hand axis.

    This can break down if the decoration size for the right hand axis (the
    margins) is very large.  There must be a math way to check for this case.

    '''
    invTransFig = fig.transFigure.inverted().transform_bbox

    axes = fig.axes

    # list of unique gridspecs that contain child axes:
    gss = set([])
    for ax in axes:
        if hasattr(ax, 'get_subplotspec'):
            gs = ax.get_subplotspec().get_gridspec()
            if gs.layoutbox is not None:
                gss.add(gs)
    if len(gss) == 0:
        warnings.warn('There are no gridspecs with layoutboxes. '
                      'Possibly did not call parent GridSpec with the fig= '
                      'keyword')


    for boo in range(2):
        # check for unoccupied gridspec slots and make ghost axes for thses
        # slots...  Do for each gs separately.  This is a pretty big kludge
        # but shoudn't have too much ill effect.  The worst is that
        # someone querrying the figure will wonder why there are more
        # axes than they thought.
        if fig.layoutbox.constrained_layout_called < 1:
            for gs in gss:
                nrows, ncols = gs.get_geometry()
                hassubplotspec = np.zeros(nrows * ncols)
                axs = []
                for ax in axes:
                    if hasattr(ax, 'get_subplotspec'):
                        if ax.get_subplotspec().get_gridspec() == gs:
                            axs += [ax]
                for ax in axs:
                    ss0 = ax.get_subplotspec()
                    if ss0.num2 is None:
                        ss0.num2 = ss0.num1
                    hassubplotspec[ss0.num1:ss0.num2+1] = 1.2
                for nn, hss in enumerate(hassubplotspec):
                    if hss < 1:
                        # this gridspec slot doesn't have an axis so we
                        # make a "ghost".
                        ax = fig.add_subplot(gs[nn])
                        ax.set_frame_on(False)
                        ax.set_xticks([])
                        ax.set_yticks([])
                        ax.set_facecolor((1., 0., 0., 0.))

        #  constrain the margins between poslayoutbox and the axis layoutbox.
        # this has to happen every call to `figure.constrained_layout` as the
        # figure may have chnaged size.
        axes = fig.axes
        for ax in axes:
            if ax.layoutbox is not None:
                pos = ax.get_position()
                tightbbox = get_axall_tightbbox(ax, renderer)
                bbox = invTransFig(tightbbox)

                ax.poslayoutbox.edit_left_margin_min(-bbox.x0 + pos.x0 + w_pad)
                ax.poslayoutbox.edit_right_margin_min(bbox.x1 - pos.x1 + w_pad)
                ax.poslayoutbox.edit_bottom_margin_min(
                                            -bbox.y0 + pos.y0 + h_pad)
                ax.poslayoutbox.edit_top_margin_min(bbox.y1-pos.y1+h_pad)

                # logging.debug('left %f' % (-bbox.x0 + pos.x0 + w_pad))
                # logging.debug('right %f' % (bbox.x1 - pos.x1 + w_pad))
                # Sometimes its possible for the solver to collapse
                # rather than expand axes, so they all have zero height
                # or width.  This stops that...  It *should* have been
                # taken into account w/ pref_width...
                if fig.layoutbox.constrained_layout_called < 1:
                    ax.poslayoutbox.constrain_height_min(20., strength='weak')
                    ax.poslayoutbox.constrain_width_min(20., strength='weak')
                    ax.layoutbox.constrain_height_min(20., strength='weak')
                    ax.layoutbox.constrain_width_min(20., strength='weak')
                    ax.poslayoutbox.constrain_top_margin(0., strength='weak')
                    ax.poslayoutbox.constrain_bottom_margin(0.,
                            strength='weak')
                    ax.poslayoutbox.constrain_right_margin(0., strength='weak')
                    ax.poslayoutbox.constrain_left_margin(0., strength='weak')

        # do layout for suptitle.
        if fig._suptitle is not None:
            sup = fig._suptitle
            bbox = invTransFig(sup.get_window_extent(renderer=renderer))
            height = bbox.y1 - bbox.y0
            sup.layoutbox.edit_height(height)

        # OK, the above lines up ax.poslayoutbox with ax.layoutbox
        # now we need to
        #   1) arrange the subplotspecs.  We do it at this level because
        #      the subplotspecs are meant to contain other dependent axes
        #      like colorbars or legends.
        #   2) line up the right and left side of the ax.poslayoutbox
        #      that have the same subplotspec maxes.

        # arrange the subplotspecs...  This is all done relative to each
        # other.  Some subplotspecs conatain axes, and others contain gridspecs
        # the ones that contain gridspecs are a set proportion of their
        # parent gridspec.  The ones that contain axes are not so constrained.

        # check for childrent that contain subplotspecs...
        if fig.layoutbox.constrained_layout_called < 1:
            figlb = fig.layoutbox
            for child in figlb.children:
                name = (child.name).split('.')[-1][:-3]
                if name == 'gridspec':
                    # farm the gridspec layout out.  Maybe bad organization
                    # and this function should be here in constrained_layout
                    layoutbox.arange_subplotspecs(child)

        # this only needs to happen once:

        if fig.layoutbox.constrained_layout_called < 1:
            fig.layoutbox.constrained_layout_called += 1
            for gs in gss:
                nrows, ncols = gs.get_geometry()
                axs = []

                # get axes in this gridspec....
                for ax in axes:
                    if hasattr(ax, 'get_subplotspec'):
                        if ax.get_subplotspec().get_gridspec() == gs:
                            axs += [ax]
                for ax in axs:
                    axs = axs[1:]
                    # now compare ax to all the axs:
                    # if a subplotspec is to the left of a subplotspec, then
                    # hstack them vstack the otehr ones.  Note this doesn't
                    # imply they are adjacent, and in some ways introduces
                    # a bunch of redundant constraints.
                    #
                    # If the subplotspecs have the same colNumXmax, then line
                    # up their right sides.  If they have the same min, then
                    # their left sides (and vertical equivalents).
                    ss0 = ax.get_subplotspec()
                    if ss0.num2 is None:
                        ss0.num2 = ss0.num1
                    rowNum0min, colNum0min = divmod(ss0.num1, ncols)
                    rowNum0max, colNum0max = divmod(ss0.num2, ncols)
                    for axc in axs:
                        if ax == axc:
                            pass
                        else:
                            ssc = axc.get_subplotspec()
                            # get the rowNums and colNums
                            rowNumCmin, colNumCmin = divmod(ssc.num1, ncols)
                            if ssc.num2 is None:
                                ssc.num2 = ssc.num1
                            rowNumCmax, colNumCmax = divmod(ssc.num2, ncols)

                            # OK, this tells us the relative layout of ax
                            # with axc
                            # Horizontal alignment:
                            if colNum0max < colNumCmin:
                                layoutbox.hstack([ss0.layoutbox,
                                                  ssc.layoutbox])
                            if colNumCmax < colNum0min:
                                layoutbox.hstack([ssc.layoutbox,
                                                  ss0.layoutbox])
                            if colNum0min == colNumCmin:
                                # we want the poslayoutboxes to line up on left
                                # side of the axes spines...
                                layoutbox.align([ax.poslayoutbox,
                                                 axc.poslayoutbox],
                                                'left')
                            if colNum0max == colNumCmax:
                                # line up right sides of poslayoutbox
                                layoutbox.align([ax.poslayoutbox,
                                                 axc.poslayoutbox],
                                                'right')
                            ####
                            # Vertical alignment:
                            if rowNum0max < rowNumCmin:
                                logging.debug('rowNum0max < rowNumCmin')
                                layoutbox.vstack([ss0.layoutbox,
                                                  ssc.layoutbox])
                            if rowNumCmax < rowNum0min:
                                logging.debug('rowNumCmax < rowNum0min')
                                layoutbox.vstack([ssc.layoutbox,
                                                  ss0.layoutbox])
                            if rowNum0min == rowNumCmin:
                                # line up top of poslayoutbox
                                logging.debug('rowNum0min == rowNumCmin')
                                layoutbox.align([ax.poslayoutbox,
                                                 axc.poslayoutbox],
                                                'top')
                            if rowNum0max == rowNumCmax:
                                # line up bottom of poslayoutbox
                                logging.debug('rowNum0max == rowNumCmax')
                                layoutbox.align([ax.poslayoutbox,
                                                 axc.poslayoutbox],
                                                'bottom')
                                #layoutbox.align([ssc.layoutbox,
                                #                 ss0.layoutbox],
                                #                'bottom')

                            ###########
                            # Now we make the widths and heights similar.
                            # This allows vertically stacked subplots to have
                            # different sizes if they occupy different ammounts
                            # of the gridspec:  i.e.
                            # gs = gridspec.GridSpec(3,1)
                            # ax1 = gs[0,:]
                            # ax2 = gs[1:,:]
                            # then drows0 = 1, and drowsC = 2, and ax2
                            # should be at least twice as large as ax1.
                            # For height, this only needs to be done if the
                            # subplots share a column.  For width if they
                            # share a row.

                            drowsC = rowNumCmax - rowNumCmin + 1
                            drows0 = rowNum0max - rowNum0min + 1
                            dcolsC = colNumCmax - colNumCmin + 1
                            dcols0 = colNum0max - colNum0min + 1

                            if drowsC > drows0:
                                logging.debug('drowsC > drows0')
                                logging.debug(drowsC / drows0)

                                logging.debug(ax.poslayoutbox)
                                logging.debug(axc.poslayoutbox)

                                if insamecolumn(ss0, ssc):
                                    axc.poslayoutbox.constrain_height_min(
                                        ax.poslayoutbox.height *
                                        drowsC / drows0)
                            elif drowsC < drows0:
                                logging.debug('drowsC < drows0')
                                logging.debug(drows0 / drowsC)
                                logging.debug(ax.poslayoutbox)
                                logging.debug(axc.poslayoutbox)
                                if insamecolumn(ss0, ssc):
                                    ax.poslayoutbox.constrain_height_min(
                                        axc.poslayoutbox.height *
                                        drows0 / drowsC)
                            else:
                                ax.poslayoutbox.constrain_height(
                                                axc.poslayoutbox.height)
                            # widths...
                            if dcolsC > dcols0:
                                if insamerow(ss0, ssc):
                                    axc.layoutbox.constrain_width_min(
                                            ax.poslayoutbox.width *
                                            dcolsC / dcols0)
                            elif dcolsC < dcols0:
                                if insamerow(ss0, ssc):
                                    ax.layoutbox.constrain_width_min(
                                            axc.poslayoutbox.width *
                                            dcols0 / dcolsC)
                            else:
                                ax.poslayoutbox.constrain_width(
                                    axc.poslayoutbox.width)

        fig.layoutbox.update_variables()
        # Now set the position of the axes...
        for ax in axes:
            if ax.layoutbox is not None:
                newpos = ax.poslayoutbox.get_rect()
                ax.set_position(newpos)
