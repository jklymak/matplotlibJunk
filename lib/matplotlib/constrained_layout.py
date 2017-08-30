
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

from __future__ import division, print_function

from matplotlib.legend import Legend
import matplotlib.transforms as transforms
import numpy as np
import matplotlib.layoutbox as layoutbox


#########
def  get_axall_tightbbox(ax, renderer):
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


######################################################
def do_constrained_layout(fig, renderer, h_pad, w_pad):

    """
    Do the constrained_layout.  Called at draw time in
     ``figure.constrained_layout()

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
    constrained separately
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
        each other, width the appropriate order.
        b) if colnum0 ==
    '''
    invTransFig = fig.transFigure.inverted().transform_bbox

    axes = fig.axes

    # list of unique gridspecs that contain child axes:
    gss = set([])
    for ax in axes:
        if hasattr(ax,'get_subplotspec'):
            gss.add(ax.get_subplotspec().get_gridspec())

    # check for unoccupied gridspec slots and make fake axes for thses
    # slots...  Do for each gs separately.
    #   This only needs to happen once.

    # the whole thing needs to happen twice, however.
    for boo in range(2):
        if fig.layoutbox.constrained_layout_called < 1:
            #print('Hi')
            for gs in gss:
                nrows, ncols = gs.get_geometry()
                hassubplotspec = np.zeros(nrows * ncols)
                axs = []
                for ax in axes:
                    if hasattr(ax,'get_subplotspec'):
                        if ax.get_subplotspec().get_gridspec() == gs:
                            axs += [ax]
                for ax in axs:
                    ss0 = ax.get_subplotspec()
                    if ss0.num2 is None:
                        ss0.num2 = ss0.num1
                    #print(ss0.num1)
                    #print(ss0.num2)

                    hassubplotspec[ss0.num1:ss0.num2+1] = 1.2
                for nn,hss in enumerate(hassubplotspec):
                    if hss < 1:
                        ax = fig.add_subplot(gs[nn])
                        ax.set_frame_on(False)
                        ax.set_xticks([])
                        ax.set_yticks([])
                        ax.set_facecolor((1.,0.,0.,0.))

        axes = fig.axes
        #  constrain the margins between poslayoutbox and the axis layoutbox.
        # this has to happen every call to `figure.constrained_layout`
        for ax in axes:
            pos = ax.get_position()
            tightbbox = get_axall_tightbbox(ax, renderer)
            #ax.get_tightbbox(renderer=renderer)
            bbox = invTransFig(tightbbox)

            ax.poslayoutbox.edit_left_margin_min(-bbox.x0+pos.x0+w_pad)
            ax.poslayoutbox.edit_right_margin_min(bbox.x1-pos.x1+w_pad)
            ax.poslayoutbox.edit_bottom_margin_min(-bbox.y0+pos.y0+h_pad)
            ax.poslayoutbox.edit_top_margin_min(bbox.y1-pos.y1+h_pad)
        # constrain the layoutbox height....
        # not sure this will work in both directions.  This may need
        # to be an editable variable rather than a set value..
        if fig._suptitle is not None:
            bbox = invTransFig(
                fig._suptitle.get_window_extent(renderer=renderer))
            height = bbox.y1 - bbox.y0
            fig._suptitle.layoutbox.edit_height(height)

        # OK, the above lines up ax.poslayoutbox with ax.layoutbox
        # now we need to
        #   1) arrange the subplotspecs.  We do it at this level because
        #      the subplotspecs are meant to contain other dependent axes
        #      like colorbars or legends.  Currently there is an error if
        #      there are un-occupied slots in the gridspec.  Probably need
        #      ghost subplotspecs....
        #   2) line up the right and left side of the ax.poslayoutbox
        #      that have the same subplotspec maxes.

        # this only needs to happen twice:
        if fig.layoutbox.constrained_layout_called < 2:
            fig.layoutbox.constrained_layout_called += 1
            for gs in gss:
                nrows, ncols = gs.get_geometry()
                axs = []
                for ax in axes:
                    if hasattr(ax,'get_subplotspec'):
                        if ax.get_subplotspec().get_gridspec() == gs:
                            axs += [ax]
                # check for unoccupied gridspec slots and make a fake
                # subplotspec for the slot.  We only want to do this once,

                for ax in axs:
                    axs = axs[1:]
                    # now compare ax to all the axs:
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
                            if colNum0max < colNumCmin:
                                layoutbox.hstack([ss0.layoutbox, ssc.layoutbox])
                            if colNumCmax < colNum0min:
                                layoutbox.hstack([ssc.layoutbox, ss0.layoutbox])
                            if colNum0min == colNumCmin:
                                # we want the poslayoutboxes to line up on left
                                # side of the axes spines...
                                layoutbox.align([  ax.poslayoutbox,
                                                   axc.poslayoutbox],
                                                'left')
                            if colNum0max == colNumCmax:
                                layoutbox.align([  ax.poslayoutbox,
                                                   axc.poslayoutbox],
                                                'right')
                            ####
                            # vertical alignment
                            if rowNumCmax > rowNum0min:
                                layoutbox.vstack([ss0.layoutbox,
                                                ssc.layoutbox])
                            if rowNum0max > rowNumCmin:
                                layoutbox.vstack([ssc.layoutbox,
                                                    ss0.layoutbox])
                            if rowNum0min == rowNumCmin:
                                layoutbox.align([  ax.poslayoutbox,
                                                   axc.poslayoutbox],
                                                'top')
                                layoutbox.align([ssc.layoutbox, ss0.layoutbox],
                                     'top')
                            if rowNum0max == rowNumCmax:
                                layoutbox.align([ ax.poslayoutbox,
                                                   axc.poslayoutbox],
                                                'bottom')
                                layoutbox.align([ssc.layoutbox, ss0.layoutbox],
                                     'bottom')
                            # make the widths similar...
                            drowsC = rowNumCmax - rowNumCmin + 1
                            drows0 = rowNum0max - rowNum0min + 1
                            dcolsC = colNumCmax - colNumCmin + 1
                            dcols0 = colNum0max - colNum0min + 1
                            if drowsC > drows0:
                                ax.poslayoutbox.constrain_height_min(
                                    axc.poslayoutbox.height * drows0 / drowsC)
                            elif drowsC < drows0:
                                axc.poslayoutbox.constrain_height_min(
                                    ax.poslayoutbox.height * drowsC / drows0)
                            else:
                                ax.poslayoutbox.constrain_height(                            axc.poslayoutbox.height)
                            if dcolsC > dcols0:
                                axc.poslayoutbox.constrain_width_min(
                                    ax.poslayoutbox.width * dcolsC / dcols0)
                            elif dcolsC < dcols0:
                                ax.poslayoutbox.constrain_width_min(
                                    axc.poslayoutbox.width * dcols0 / dcolsC)
                            else:
                                ax.poslayoutbox.constrain_width(
                                    axc.poslayoutbox.width)


                    ## Sometimes its possible for the solver to collapse
                    # rather than expand axes, so they all have zero height
                    # or width.  This stops that...  It *should* have been
                    # taken into account w/ pref_width...

                    ax.poslayoutbox.constrain_height_min(20., strength='weak')
                    ax.poslayoutbox.constrain_width_min(20., strength='weak')


        # subplotlayouts = gs.layoutbox.find_child_subplots()
        # if len(subplotlayouts) > 1:
        #     # pass
        #     layoutbox.match_margins(subplotlayouts, levels=2)
        # and update the layout for this gridspec.
        #gs.layoutbox.update_variables()

        fig.layoutbox.update_variables()
        # Now set the position of the axes...
        #fig.layoutbox.solver.dump()
        #layoutbox.print_tree(fig.layoutbox)
        for ax in axes:
            newpos = ax.poslayoutbox.get_rect()
            ax.set_position(newpos)
