"""
=========================
Date Precision and Epochs
=========================

Matplotlib can handle `.datetime` objects and `numpy.datetime64` objects using
a unit converter that recognizes these dates and converts them to floating
point numbers. By deafult this conversion returns a float that is days
since "0000-01-01T00:00:00".  This has resolution implications for modern
dates:  "2000-01-01" in this time frame is 730120, and a 64-bit floating point
number has a resolution of 2^{-52}, or approximately 14 microseconds.

"""
import datetime
import dateutil
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#############################################################################
# Datetime
# --------
#
# Python `.datetime` objects have microsecond reesolution, so by default
# matplotlib dates cannot round-trip full-resolution datetime objects:

date1 = datetime.datetime(2000, 1, 1, 0, 10, 0, 12,
                          tzinfo=dateutil.tz.gettz('UTC'))
mdate1 = mdates.date2num(date1)
print('Before Roundtrip: ', date1, 'Matplotlib date:', mdate1)
date2 = mdates.num2date(mdate1)
print('After Roundtrip:  ', date2)

#############################################################################
# Note this is only a round-off error, and there is no problem for
# dates closer to the epoch:

date1 = datetime.datetime(10, 1, 1, 0, 10, 0, 12,
                          tzinfo=dateutil.tz.gettz('UTC'))
mdate1 = mdates.date2num(date1)
print('Before Roundtrip: ', date1, 'Matplotlib date:', mdate1)
date2 = mdates.num2date(mdate1)
print('After Roundtrip:  ', date2)

#############################################################################
# If a user wants to use modern dates at microsecond precision, they
# can change the epoch.  However, note that calling `.set_epoch` yields an
# error here.  Thats because mixing epochs in a script is confusing, so
# we attach a sentinel that doesn't let it be changed after any dates
# code has been run.

try:
    mdates.set_epoch('1990-01-01')
except RuntimeError as e:
    print('RuntimeError:', str(e))

#############################################################################
# For this tutorial, we reset the sentinel.
# .. warning:: Users (and downstream libraries) should avoid using the private
# method of resetting sentinel.

mdates._reset_epoch()  # Don't do this.  Just being done for this tutorial.

mdates.set_epoch('1990-01-01')
date1 = datetime.datetime(2000, 1, 1, 0, 10, 0, 12,
                          tzinfo=dateutil.tz.gettz('UTC'))
mdate1 = mdates.date2num(date1)
print('Before Roundtrip: ', date1, 'Matplotlib date:', mdate1)
date2 = mdates.num2date(mdate1)
print('After Roundtrip:  ', date2)

#############################################################################
# datetime64
# ----------
#
# `numpy.datetime64` objects have microsecond precision for a much larger
# timespace than `.datetime` objects.  However, currently Matplotlib time is
# only converted back to datetime objects, which have microsecond resolution,
# and years that only span 0000 to 9999.

mdates._reset_epoch()  # Don't do this.  Just being done for this tutorial.

mdates.set_epoch('1990-01-01')

date1 = np.datetime64('2000-01-01T00:10:00.000012')
mdate1 = mdates.date2num(date1)
print('Before Roundtrip: ', date1, 'Matplotlib date:', mdate1)
date2 = mdates.num2date(mdate1)
print('After Roundtrip:  ', date2)

#############################################################################
# Plotting
# --------
#
# This all of course has an effect on plotting.  With the default epoch
# the times are rounded, leading to jumps in the data:

mdates._reset_epoch()  # Don't do this.  Just being done for this tutorial.

x = np.arange('2000-01-01T00:00:00.0', '2000-01-01T00:00:00.000100',
              dtype='datetime64[us]')
y = np.arange(0, len(x))
fig, ax = plt.subplots(constrained_layout=True)
ax.plot(x, y)
ax.set_title('Epoch: ' + mdates.get_epoch())
plt.setp(ax.xaxis.get_majorticklabels(), rotation=40)
plt.show()

#############################################################################
# For a more recent epoch, the plot is smooth:

mdates._reset_epoch()  # Don't do this.  Just being done for this tutorial.

mdates.set_epoch('1999-01-01')
fig, ax = plt.subplots(constrained_layout=True)
ax.plot(x, y)
ax.set_title('Epoch: ' + mdates.get_epoch())
plt.setp(ax.xaxis.get_majorticklabels(), rotation=40)
plt.show()

mdates._reset_epoch()  # Don't do this.  Just being done for this tutorial.

#############################################################################
# ------------
#
# References
# """"""""""
#
# The use of the following functions, methods and classes is shown
# in this example:

matplotlib.dates.num2date
matplotlib.dates.date2num
matplotlib.dates.set_epoch
