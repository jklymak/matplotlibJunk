API changes for ``constrained_layout``
----------------------------------------

The new constrained_layout functionality has some minor (largely backwards-
compatible) API changes.  See
:ref:`sphx_glr_tutorials_intermediate_constrainedlayout_guide.py` for
more details on this functionality.


New ``plt.figure`` and ``plt.subplots`` kwarg: ``constrained_layout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:meth:`~matplotlib.pyplot.figure` and :meth:`~matplotlib.pyplot.subplots`
can now be called with ``constrained_layout=True`` kwarg to enable
constrained_layout.

New ``ax.set_position`` behaviour
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:meth:`~matplotlib.axes.set_position` now makes the specified axis no
longer responsive to constrained_layout, consistent with the idea that the
user wants to place an axis manually.

Internally, this means that old ``ax.set_position`` calls *inside* the library
are changed to private ``ax._set_position`` calls.

New ``fig`` kwarg for ``GridSpec``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to facilitate constrained_layout ``GridSpec`` now accepts a
``fig`` keyword.  This is backwards compatible, in that not doing this will
simply cause constrained_layout to not operate on the subplots orgainzed by
this ``GridSpec``. instance.  Routines that use ``GridSpec`` (i.e. ``ax.subplots``)
have been modified to pass the figure to ``GridSpec``.
