# -*- coding: utf-8 -*-
"""

"""
from __future__ import division, print_function
import kiwisolver as kiwi
import numpy as np
import matplotlib
#import matplotlib.gridspec as gridspec



# plt.close('all')


class LayoutBox(object):
    """
    Basic rectangle representation using kiwi solver variables
    """



    def __init__(self, parent=None, name='', tightwidth=False,
                tightheight=False, artist=None,
                 lower_left=(0, 0), upper_right=(1, 1), pos=False,
                 subplot=False):
        Variable = kiwi.Variable
        self.parent = parent
        self.name = name
        sn = self.name + '_'
        if parent is None:
            self.solver = kiwi.Solver()
        else:
            self.solver = parent.solver
            parent.add_child(self)
        # keep track of artist associated w/ this layout.  Can be none
        self.artist = artist
        # keep track if this box is supposed to be a pos that is constrained by the parent.
        self.pos = pos
        # keep track of whether we need to match this subplot up with others.
        self.subplot = subplot

        self.top = Variable(sn + 'top')
        self.bottom = Variable(sn + 'bottom')
        self.left = Variable(sn + 'left')
        self.right = Variable(sn + 'right')

        self.width = Variable(sn + 'width')
        self.height = Variable(sn + 'height')
        self.h_center = Variable(sn + 'h_center')
        self.v_center = Variable(sn + 'v_center')

        self.min_width = Variable(sn + 'min_width')
        self.min_height = Variable(sn + 'min_height')
        self.pref_width = Variable(sn + 'pref_width')
        self.pref_height = Variable(sn + 'pref_height')
        self.left_margin = Variable(sn + 'left_margin')
        self.right_margin = Variable(sn + 'right_margin')
        self.bottom_margin = Variable(sn + 'bottom_margin')
        self.top_margin = Variable(sn + 'top_margin')

        right, top = upper_right
        left, bottom = lower_left
        self.tightheight = tightheight
        self.tightwidth = tightwidth
        self.add_constraints()
        self.children = []
        self.subplotspec = None
        if self.pos:
            self.constrain_margins()

    def constrain_margins(self):
        """
        Only do this for poss.  This sets a variable distance
        margin between the spline and the outer edge of the axis
        """
        sol = self.solver

        #left
        if not sol.hasEditVariable(self.left_margin):
            sol.addEditVariable(self.left_margin, 'medium')
            sol.suggestValue(self.left_margin, 0.0001)
        c = (self.left_margin == self.left - self.parent.left)
        self.solver.addConstraint(c | 'required')
        #right
        if not sol.hasEditVariable(self.right_margin):
            sol.addEditVariable(self.right_margin, 'medium')
            sol.suggestValue(self.right_margin, 0.0001)
        c = (self.right_margin == self.parent.right - self.right)
        self.solver.addConstraint(c | 'required')
        #bottom
        if not sol.hasEditVariable(self.bottom_margin):
            sol.addEditVariable(self.bottom_margin, 'medium')
            sol.suggestValue(self.bottom_margin, 0.0001)
        c = (self.bottom_margin == self.bottom - self.parent.bottom)
        self.solver.addConstraint(c | 'required')
        #top
        if not sol.hasEditVariable(self.top_margin):
            sol.addEditVariable(self.top_margin, 'medium')
            sol.suggestValue(self.top_margin, 0.0001)
        c = (self.top_margin == self.parent.top - self.top)
        self.solver.addConstraint(c | 'required')

    def add_child(self, child):
        self.children += [child]

    def remove_child(self, child):
        try:
            self.children.remove(child)
        except ValueError:
            print("Tried to remove child that doesn't belong to parent")

    def add_constraints(self):
        sol = self.solver
        # never let width and height go negative.
        for i in [self.min_width, self.min_height]:
            sol.addEditVariable(i, 1e9)
            sol.suggestValue(i, 0.0)
        # define relation ships between things thing width and right and left
        self.hard_constraints()
        self.soft_constraints()
        if self.parent:
            self.parent_constrain()
        sol.updateVariables()

    def parent_constrain(self):
        parent = self.parent
        eps = 0.0000000
        hc = [self.left >= parent.left+eps,
              self.bottom >= parent.bottom +eps,
              self.top <= parent.top - eps,
              self.right <= parent.right - eps]
        for c in hc:
            self.solver.addConstraint(c | 'required')

    def hard_constraints(self):
        hc = [self.width == self.right - self.left,
              self.height == self.top - self.bottom,
              self.h_center == (self.left + self.right) * 0.5,
              self.v_center == (self.top + self.bottom) * 0.5,
              self.width >= self.min_width,
              self.height >= self.min_height]
        for c in hc:
            self.solver.addConstraint(c | 'required')

    def soft_constraints(self):
        sol = self.solver
        if self.tightwidth:
            suggest = 0.
        else:
            suggest = 1.
        c = [(self.pref_width == suggest)]
        for i in c:
            sol.addConstraint(i | 'strong')
        if self.tightheight:
            suggest = 0.
        else:
            suggest = 1.
        c = [(self.pref_height == suggest)]
        for i in c:
            sol.addConstraint(i | 'strong')

        c = [(self.pref_width == self.width),
             (self.pref_height == self.height)]
        for i in c:
            sol.addConstraint(i | 'weak')

    def set_parent(self, parent):
        ''' replace the parent of this with the new parent
        '''
        self.parent = parent
        self.parent_constrain()

    def set_geometry_soft(self, left, bottom, right, top, strength='medium'):
        sol = self.solver
        for i in [self.top, self.bottom,
                  self.left, self.right]:
            if not sol.hasEditVariable(i):
                sol.addEditVariable(i, strength)
        sol.suggestValue(self.top, top)
        sol.suggestValue(self.bottom, bottom)
        sol.suggestValue(self.left, left)
        sol.suggestValue(self.right, right)
        sol.updateVariables()

    def set_geometry(self, left, bottom, right, top, strength='strong'):
        hc = [self.left == left,
            self.right == right,
            self.bottom == bottom,
            self.top == top]
        for c in hc:
            self.solver.addConstraint((c | strength))
        self.solver.updateVariables()

    def set_left_margin(self, margin, strength='strong'):
        c = (self.left == self.parent.left + margin )
        self.solver.addConstraint(c | strength)

    def set_left_margin_min(self, margin):
        self.solver.suggestValue(self.left_margin, margin )
        #c = (self.left >= self.parent.left + margin )
        #self.solver.addConstraint(c | 'strong')

    def set_right_margin(self, margin, strength='strong'):
        c = (self.right == self.parent.right - margin )
        self.solver.addConstraint(c | strength)

    def set_right_margin_min(self, margin):
        self.solver.suggestValue(self.right_margin, margin )

    def set_bottom_margin(self, margin, strength='strong'):
        c = (self.bottom == self.parent.bottom + margin )
        self.solver.addConstraint(c | strength)

    def set_bottom_margin_min(self, margin):
        self.solver.suggestValue(self.bottom_margin, margin )

    def set_top_margin(self, margin, strength='strong'):
        c = (self.top == self.parent.top - margin )
        self.solver.addConstraint(c | strength)

    def set_top_margin_min(self, margin):
        self.solver.suggestValue(self.top_margin, margin )

    def set_width_margins(self,margin):
        self.set_left_margin(margin)
        self.set_right_margin(margin)

    def set_height_margins(self,margin):
        self.set_top_margin(margin)
        self.set_bottom_margin(margin)

    def set_margins(self,margin):
        self.set_height_margin(margin)
        self.set_width_margin(margin)

    def get_rect(self):
        return (self.left.value(), self.bottom.value(),
                self.width.value(), self.height.value())

    def update_variables(self):
        '''
        Update *all* the variables that are part of the solver this LayoutBox
        is created with
        '''
        self.solver.updateVariables()

    def set_height(self, height, strength='strong'):
        c = (self.height == height)
        self.solver.addConstraint(c | strength)

    def set_width(self, width, strength='strong'):
        c = (self.width == width)
        self.solver.addConstraint(c | strength)

    def set_left(self, left):
        c = (self.left == left)
        self.solver.addConstraint(c | 'strong')

    def set_bottom(self, bottom):
        c = (self.bottom == bottom)
        self.solver.addConstraint(c | 'strong')

    def find_child_subplots(self):
        '''
        Find children of this layout box that are subplots.  We want to line
        poss up, and this is an easy way to find them all.
        '''
        if self.subplot:
            subplots = [self]
        else:
            subplots = []
        for child in self.children:
            subplots += child.find_child_subplots()
        return subplots


    def layout_from_subplotspec(self, subspec, name='', artist=None, pos=False):
        '''  Make a layout box from a subplotspec. The layout box is
        constrained to be a fraction of the width/height of the parent,
        and be a fraction of the parent width/height from the left/bottom
        of the parent.  Therefore the parent can move around and the
        layout for the subplot spec should move with it.

        The parent is *usually* the gridspec that made the subplotspec.??
        '''
        lb = LayoutBox(parent=self, name=name, artist=artist, pos=pos)
        gs = subspec.get_gridspec()
        nrows, ncols = gs.get_geometry()
        parent = self.parent

        # from gridspec.  prob should be new method in gridspec
        left = 0.0
        right = 1.0
        bottom = 0.0
        top = 1.0
        totWidth = right-left
        totHeight = top-bottom
        hspace = 0.
        wspace = 0.

        # calculate accumulated heights of columns
        cellH = totHeight/(nrows + hspace*(nrows-1))
        sepH = hspace*cellH

        if gs._row_height_ratios is not None:
            netHeight = cellH * nrows
            tr = float(sum(gs._row_height_ratios))
            cellHeights = [netHeight*r/tr for r in gs._row_height_ratios]
        else:
            cellHeights = [cellH] * nrows

        sepHeights = [0] + ([sepH] * (nrows-1))
        cellHs = np.add.accumulate(np.ravel(list(zip(sepHeights, cellHeights))))

        # calculate accumulated widths of rows
        cellW = totWidth/(ncols + wspace*(ncols-1))
        sepW = wspace*cellW

        if gs._col_width_ratios is not None:
            netWidth = cellW * ncols
            tr = float(sum(gs._col_width_ratios))
            cellWidths = [netWidth*r/tr for r in gs._col_width_ratios]
        else:
            cellWidths = [cellW] * ncols

        sepWidths = [0] + ([sepW] * (ncols-1))
        cellWs = np.add.accumulate(np.ravel(list(zip(sepWidths, cellWidths))))

        figTops = [top - cellHs[2*rowNum] for rowNum in range(nrows)]
        figBottoms = [top - cellHs[2*rowNum+1] for rowNum in range(nrows)]
        figLefts = [left + cellWs[2*colNum] for colNum in range(ncols)]
        figRights = [left + cellWs[2*colNum+1] for colNum in range(ncols)]

        rowNum, colNum =  divmod(subspec.num1, ncols)
        figBottom = figBottoms[rowNum]
        figTop = figTops[rowNum]
        figLeft = figLefts[colNum]
        figRight = figRights[colNum]

        if subspec.num2 is not None:

            rowNum2, colNum2 =  divmod(subspec.num2, ncols)
            figBottom2 = figBottoms[rowNum2]
            figTop2 = figTops[rowNum2]
            figLeft2 = figLefts[colNum2]
            figRight2 = figRights[colNum2]

            figBottom = min(figBottom, figBottom2)
            figLeft = min(figLeft, figLeft2)
            figTop = max(figTop, figTop2)
            figRight = max(figRight, figRight2)
        # Ok, these are numbers relative to 0,0,1,1.  Need to constrain
        # relative to parent.

        width = figRight - figLeft
        height = figTop - figBottom

        eps = 0.001
        cs = [lb.left   == self.left  + self.width * figLeft,
            lb.bottom  == self.bottom + self.height * figBottom,
            lb.width == self.width * width ,
            lb.height == self.height * height ]
        for c in cs:
            self.solver.addConstraint((c | 'strong'))

        return lb


    def layout_axis_right(self, ax, shrink=0.6, padding=None, toppad=0, bottompad=0, leftpad=0, rightpad=0):
        '''
        return cblb, cbposlb

        Layout ax to the right of this layout box.
        '''
        if padding:
            toppad = padding
            bottompad = padding
            leftpad = padding
            rightpad = padding
        cblb = LayoutBox(
            parent=self.parent,
            name=self.parent.name+'.right',
            artist=ax,
            tight=True)
        # this is the location for the colorbar pos
        cbposlb = LayoutBox(
            parent=cblb,
            name=cblb.name+'.rightpos',
            pos=False)
        # this is really a pos, but we don't want it to share margins
        c = (self.right  <= cblb.left)
        self.solver.addConstraint(c | 'required')
        # hstack([self,cblb], padding=0.)

        cbposlb.set_height(self.height*shrink)
        align([self,cbposlb],'v_center')

        if 1:
            fig = ax.get_figure()
            renderer = fig.canvas.get_renderer()
            pos = ax.get_position()
            invTransFig = fig.transFigure.inverted().transform_bbox
            bbox = invTransFig(ax.get_tightbbox(renderer=renderer))

            # set the width of the parent box.
            c = (cbposlb.width  == 0.05 * self.width)
            self.solver.addConstraint(c | 'strong')
            c = (cblb.width  == bbox.x1-bbox.x0)
            self.solver.addConstraint(c | 'medium')
            if 0:
                cbposlb.set_left_margin(-bbox.x0+pos.x0+leftpad)
                cbposlb.set_right_margin(bbox.x1-pos.x1+rightpad)
                cbposlb.set_bottom_margin_min(-bbox.y0+pos.y0+bottompad)
                cbposlb.set_top_margin_min(bbox.y1-pos.y1+toppad)

        return cblb, cbposlb


    def layout_axis_subplotspec(self, subspec, name='', ax=None, pad=None, toppad=0, bottompad=0, leftpad=0, rightpad=0):
        if pad:
            toppad = pad
            bottompad = pad
            leftpad = pad
            rightpad = pad
        sslb = self.layout_from_subplotspec(subspec,
                name=self.name+'.'+name+'.sslb', artist=subspec)
        # this is th contaier for the axis itself
        axlb = LayoutBox(parent=sslb, name=sslb.name+'.axlb', artist=ax)
        # this is the location needed for the pos.
        axposlb = LayoutBox(parent=axlb,
            name=axlb.name+'.axposlb', artist=None)

        # now do the layout based on ax...
        fig = ax.get_figure()
        renderer = fig.canvas.get_renderer()
        pos = ax.get_position()
        invTransFig = fig.transFigure.inverted().transform_bbox
        bbox = invTransFig(ax.get_tightbbox(renderer=renderer))
        # leftpad = 0; rightpad=0; bottompad=0.; toppad=0.
        axposlb.set_left_margin_min(-bbox.x0+pos.x0+leftpad)
        axposlb.set_right_margin_min(bbox.x1-pos.x1+rightpad)
        axposlb.set_bottom_margin_min(-bbox.y0+pos.y0+bottompad)
        axposlb.set_top_margin_min(bbox.y1-pos.y1+toppad)

        return sslb, axlb, axposlb

    def place_children(self):
        for child in self.children:
            child.place_children()
            ax = child.artist
            if (child and hasmethod(ax,'set_position')):
                ax.set_position(child.get_rect())

    def __repr__(self):
        args = (self.name, self.left.value(), self.bottom.value(),
                self.right.value(), self.top.value(), self.pref_width.value(),
                self.artist, self.pos)
        return 'LayoutBox: %40s, (left: %1.2f) (bot: %1.2f) (right: %1.2f) (top: %1.2f) (pref_width: %1.2f) (artist: %s) (pos?: %s)'%args

def hstack(boxes, padding=0):
    '''
    Stack LayoutBox instances from left to right
    '''

    for i in range(1,len(boxes)):
        c = (boxes[i-1].right + padding <= boxes[i].left)
        boxes[i].solver.addConstraint(c | 'strong')

def vstack(boxes, padding=0):
    '''
    Stack LayoutBox instances from top to bottom
    '''

    for i in range(1,len(boxes)):
        c = (boxes[i-1].bottom - padding >= boxes[i].top)
        boxes[i].solver.addConstraint(c | 'strong')

def match_heights(boxes, height_ratios=None, strength='medium'):
    '''
    Stack LayoutBox instances from top to bottom
    '''

    if height_ratios == None:
        height_ratios = np.ones(len(boxes))
    for i in range(1,len(boxes)):
        c = (boxes[i-1].height ==
                boxes[i].height*height_ratios[i-1]/height_ratios[i])
        boxes[i].solver.addConstraint(c | strength)

def match_widths(boxes, width_ratios=None, strength='medium'):
    '''
    Stack LayoutBox instances from top to bottom
    '''

    if width_ratios == None:
        width_ratios = np.ones(len(boxes))
    for i in range(1,len(boxes)):
        c = (boxes[i-1].width ==
                boxes[i].width*width_ratios[i-1]/width_ratios[i])
        boxes[i].solver.addConstraint(c | strength)

def vstackeq(boxes, padding=0, height_ratios=None):
    vstack(boxes,padding=padding)
    match_heights(boxes, height_ratios=height_ratios)

def hstackeq(boxes, padding=0, width_ratios=None):
    hstack(boxes,padding=padding)
    match_widths(boxes, width_ratios=width_ratios)

def align(boxes, attr):
    cons = []
    for box in boxes[1:]:
        cons= (getattr(boxes[0], attr) == getattr(box, attr))
        boxes[0].solver.addConstraint(cons | 'medium')



def match_top_margins(boxes, levels=1):
    box0 = boxes[0]
    top0 = box0
    for n in range(levels):
        top0 = top0.parent
    for box in boxes[1:]:
        topb = box
        for n in range(levels):
            topb = topb.parent
        c = (box0.top-top0.top == box.top-topb.top)
        box0.solver.addConstraint(c | 'strong')

def match_bottom_margins(boxes, levels=1):
    box0 = boxes[0]
    top0 = box0
    for n in range(levels):
        top0 = top0.parent
    for box in boxes[1:]:
        topb = box
        for n in range(levels):
            topb = topb.parent
        c = (box0.bottom-top0.bottom == box.bottom-topb.bottom)
        box0.solver.addConstraint(c | 'strong')

def match_left_margins(boxes, levels=1):
    box0 = boxes[0]
    top0 = box0
    for n in range(levels):
        top0 = top0.parent
    for box in boxes[1:]:
        topb = box
        for n in range(levels):
            topb = topb.parent
        c = (box0.left-top0.left == box.left-topb.left)
        box0.solver.addConstraint(c | 'strong')

def match_right_margins(boxes, levels=1):
    box0 = boxes[0]
    top0 = box0
    for n in range(levels):
        top0 = top0.parent
    for box in boxes[1:]:
        topb = box
        for n in range(levels):
            topb = topb.parent
        c = (box0.right-top0.right == box.right-topb.right)
        box0.solver.addConstraint(c | 'strong')

def match_width_margins(boxes, levels=1):
    match_left_margins(boxes, levels=levels)
    match_right_margins(boxes, levels=levels)

def match_height_margins(boxes, levels=1):
    match_top_margins(boxes, levels=levels)
    match_bottom_margins(boxes, levels=levels)

def match_margins(boxes, levels=1):
    match_width_margins(boxes, levels=levels)
    match_height_margins(boxes, levels=levels)

def constrained_layout(fig, parent=None, axs=None, leftpad=0, bottompad=0,
                      rightpad=0, toppad=0, pad=None, name=None):
    '''
    '''
    import matplotlib
    if isinstance(axs,list):
        pass
    else:
        axs = [axs]

    if parent is None:
        parentlb = LayoutBox(parent=None, name=name+'figlb')
        parentlb.set_geometry(0., 0., 1., 1.)
    else:
        parentlb = parent
    if pad != None:
        leftpad = pad
        righttpad = pad
        toppad = pad
        bottompad = pad

    # check to get the container subplot spec (or the figure)
    ss = axs[0].get_subplotspec()


    axlbs = []
    poslbs = []

    renderer = fig.canvas.get_renderer()
    for n,ax in enumerate(axs):
        ss=ax.get_subplotspec()

        axlb = parentlb.layout_from_subplotspec(ss, name=name+'axlb%d'%n)
        # OK, we have already pre-plotted the axes, so we know their positions and their bbox
        pos = ax.get_position()
        invTransFig = fig.transFigure.inverted().transform_bbox
        bbox = invTransFig(ax.get_tightbbox(renderer=renderer))

        poslb = LayoutBox(parent=axlb, name=name+'poslb%d'%n)
        poslb.set_left_margin_min(-bbox.x0+pos.x0+leftpad)
        poslb.set_right_margin_min(bbox.x1-pos.x1+rightpad)
        poslb.set_bottom_margin_min(-bbox.y0+pos.y0+bottompad)
        poslb.set_top_margin_min(bbox.y1-pos.y1+toppad)

        axlbs += [axlb]
        poslbs += [poslb]


    # make all the margins match
    match_margins(poslbs)
    # run the solver
    parentlb.update_variables()

    # OK, this should give us the new positions that will fit the axes...

    for poslb,ax in zip(poslbs,axs):
        ax.set_position(poslb.get_rect())

def randid():
    '''
    Generate a short uuid for layoutbox objects...
    '''

    return ('%04d'%(np.random.rand(1)*1000.))

def print_children(lb):
    '''
    Print the children of the layoutbox
    '''
    print(lb)
    for child in lb.children:
        print_children(child)

def print_tree(lb):
    '''
    Print the tree of layoutboxes
    '''

    if lb.parent is None:
        print_children(lb)
    else:
        print_tree(lb.parent)

def plot_children(fig, box, level=0, printit=True):
    '''
    Simple plotting to show where boxes are
    '''
    import matplotlib
    import matplotlib.pyplot as plt

    if isinstance(fig, matplotlib.figure.Figure):
        ax = fig.add_axes([0., 0., 1., 1.])
    else:
        ax = fig
    import matplotlib.patches as patches
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    if printit:
        print("Level:", level)
    for child in box.children:
        rect = child.get_rect()
        if printit:
            print(child)
        ax.add_patch(
            patches.Rectangle(
                (child.left.value(), child.bottom.value()),   # (x,y)
                child.width.value(),          # width
                child.height.value(),          # height
                fc = 'none',
                ec = colors[level]
            )
        )
        if level%2 == 0:
            ax.text(child.left.value(), child.bottom.value(), child.name,
                   size=12-level, color=colors[level])
        else:
            ax.text(child.right.value(), child.top.value(), child.name,
                    ha='right', va='top', size=12-level, color=colors[level])

        plot_children(ax, child, level=level+1, printit=printit)
