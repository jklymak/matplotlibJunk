Constrained Layout Manager
---------------------------

A new method to automatically decide spacing between subplots and their
organizing ``GridSpec`` instances has been added.  It is meant to
replace the venerable ``tight_layout`` method.  It is invoked via
a new ``plt.figure(constrained_layout=True)`` kwarg to
:class:`~matplotlib.figure.Figure` or :method:`~matplotlib.figure.subplots`.
There are new ``rcParams`` for this package, and spacing can be
more finely tuned with the new
:method:`~matplotlib.figure.set_constrained_layout_pads`.

Features include:

  - Automatic spacing for subplots with a fixed-size padding in inches around
    subplots and all their decorators, and space between as a fraction
    of subplot size between subplots.
  - Spacing for ``suptitle``, and colorbars that are attached to
    more than one axes.
  - Nested ``GridSpec`` layouts using ``GridSpecFromSubplotSpec``.

For more details and capabilities please see the new tutorial:
:ref:`sphx_glr_tutorials_intermediate_constrainedlayout_guide.py`
