
# Units MEP

## Scope

It is desirable for data put into Matplotlib to have units attached to them, and then, when plotted, to convert the data with units to screen coordinates.  This data with units can either be explicit units, like a numpy array where the units of the data is kilometers, but we want to be able to change an axes to miles, or it can be implicit, i.e. a list of dates that we want to be able to plot, or a list of strings that we want plotted as integers ("categories").  There are four parts to this process:

1. inputting the data and the unit information, and then storing it in a way that allows conversion to different units later. i.e. the user changes an axis from km to miles we want to be able to reconvert w/o losing data.
2. Choosing a converter for the axis.
2. Converting the data at the correct time to floats for plotting
3. Displaying the axis information correctly (i.e. ticker locators and formatters, appropriate to the units of the data type).



### Inputing and storing unitized data

Here we are imagining a call like

```python
ax.scatter(x, y, s=s)
```

The variables `x`, `y`, and `s` could all have units (they don't need to).  For a bare call like this, they would need to have the units indicated in the datatype somehow.  For instance for times, if `type(x)` is `numpy.datenum64` we can detect that and know that these are date units.  

**Proposal:** A second way to enter units would be via passing a tuple to `x` etc i.e. `x=(xdata, 'km')`.  This would be a way to explicitly set the units of `x`.  

Internally, we are going to convert `xdata` to a numpy array, depending on the converter assigned to the `ax.xaxis`.  That conversion should happen when the data is assigned to the axes (via `scatter` for instance) and if the units or converter on the `xaxis` is changed.  Because we can't count on the converter between the unitized data and the internal numpy array being linear or even one-to-one, we must store the original data for future conversion.  

**Proposal** We make a new `userdata` class:

```
userdata.values      # original data in its original form (whatever that might have been)
userdata.units       # original units as specified by the user.  
userdata.mplvalues   # numpy n-d array (maybe masked array?) representing the data after units
                     # conversion (but before axes transforms)
```

This data class would be what gets put into the Artists like `self._x` etc.  i.e. `Line2D` has `self._xorig`, `self._x`, which kind of do the same thing; this would just contain that info, make it homogenized across artists, and allow units information to be explicitly attached to the data.


### Choosing and setting a converter and units.

The axis (i.e. xaxis) needs to have one converter attached to it that takes user data and converts to n-d numpy arrays (usually 1-d). We presently have a converter registry that tries to do this automatically, so this would be set by the first call that assigns data to the axis; so `scatter(x=(xdata, 'km'), y, s)` would look for a converter that takes 'km' units in the registry.  If one didn't exist, it would use a default converter.  

**Proposal** Of course we'd like to be able to also set a converter manually to override anything that is done automatically.  For this we should make a  `xaxis.set_converter(ConverterInterface)` method for the xaxis (and a `get_converter`).  

**Proposal** We would also like to be able to specify the units for the axis.  Right now this is done in the JPL units, but not in subsequent uses of units in the codebase (i.e. datetimes just have one units, as do categories).  We should allow specification of units, probably simply via a string: `xaxis.set_units('miles')`.  The xaxis units converter will have to be able to accept those units.

**Proposal** When either `xaxis.set_converter` or `xaxis.set_units` are called, the suggestion would be that all the artists in the axes are looped through and converted.  An alternative would be to wait until draw time, but draws are quite frequent, whereas axis unit changes are likely infrequent.

### Displaying axis information correctly

This is currently pretty well done; when a Converter is registered it sets the tickLocator and tickFormatter for the axis.  

## Extensions

There is no reason this should not extend beyond 1-d axes data.  2-D pcolor/image data could also be stored this way, with the attendant conversion affecting the colorbar.  

## Example

The base converter class would be similar to current `ConversionInterface` class.  







```python

```
