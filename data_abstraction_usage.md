About
=====

This document shows examples of usage of the new API for the abstraction of
data objects, such that they no longer have to conform to the paradigm of local
n-dimensional Numpy arrays, but can then be based for example on remote data,
or non-regularly-gridded data.

The examples below assume that the data object already exists and is called
``data`` - details of how to set up these objects is beyond the scope of this
document.

Basic usage
===========

Given a data object ``data``, we can check what components this data contains::

    >>> data.components
    [density, temperature, pressure]
    
Each component is a set of values for a particular quantity. We can distinguish
two kinds of data: continuous data, where we can find a value for these
quantities at any point, and discrete data, where we can't. We can check
whether a dataset is considered continuous or discrete by checking the
``continuous`` property::

    >>> data.continuous
    True
    
Examples of continous data would include any type of gridded data such as data
cubes, or grid-based simulations, while discrete data would include
catalogs/collections of individual objects. If a dataset is continuous, we need
to find out the coordinate systems in which the values are defined (and which
we can use to extract data)::

    >>> data.coordinates
    [world1, world2]
    >>> data.axes[world1]
    ('z', 'y', 'x')

In the above case, the data can be represented in two different coordinate
systems, ``world1`` and ``world2``. These could be for example a coordinate
system with (x, y, z) distances in kpc, or a coordinate system with (x, y, z)
values in relative units compared to a distance scale. We can find out about
the total extent of the data in a particular coordinate system.

    >>> data.extent[world1]
    [(-3, 3), (-4, 4), (-2, 2)]

Note that this will not work if the data is discrete. Continuing to assume that
the data is continuous, we can ask for a fixed resolution buffer of the data -
we are in particular interested in a slice for a particular y position (y=0)
and with a resolution of (20, 20) over the extent of the data. This can be
extracted with:

    >>> image = data.compute_frb('density',
                                 slices=[(-3, 3, 20), 0, (-2, 2, 20)])



