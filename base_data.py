"""
About
=====

This document describes a new API for the abstraction of data objects, such
that they no longer have to conform to the paradigm of local n-dimensional
Numpy arrays, but can then be based for example on remote data, or
non-regularly-gridded data.

The implementation will be done by defining a ``BaseData`` abstract base class
which defines the main API. The ``Data`` class will then be a sub-class that
implements a class for regular Numpy arrays and will be compatible (as much as
possible) with the current Data class.
"""

from abc import ABCMeta, abstractmethod, abstractproperty


@six.add_metaclass(ABCMeta)
class BaseData(object):
    
    @abstractproperty
    def components(self):
        """
        A list of all ComponentIDs in the data
        """
        raise NotImplementedError()

    @abstractproperty
    def derived_components(self):
        """
        A list of all ComponentIDs for derived components in the data
        """
        raise NotImplementedError()
    
    @abstractproperty
    def subsets(self):
        """
        A list of all Subset objects. A Subset object is one that contains
        information about how the subset is conceptually defined (for example a
        polygon selection in 2D), as well as a name. It can be passed to the
        ``compute_*`` methods to extract information only about subsets.
        """
        raise NotImplementedError()
    
    @abstractmethod
    def compute_histogram(self, component_ids, bins=None, limits=None, subset=None):
        """
        Compute an n-dimensional histogram for the component.
        
        Parameters
        ----------
        component_ids : iterable of ComponentID
            The component ID(s) for which to compute a histogram. If n
            components are passed, an n-dimensional histogram is computed.
        bins : iterable of int, optional
            The number of bins for each component. For categorical components,
            the number of bins should be set to None.
        limits : iterable, optional
            The range of values inside which to compute the histogram. This
            should be an iterable with ``(min, max)`` items for each dimension.
        subset : Subset, optional
            The subset, if applicable. If set, the histogram will include only
            values in the subset.
            
        Notes
        -----
        We could have a way to specify the desired accuracy, so that histograms
        can be determined from subsets of huge datasets.
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_frb(self, component_id, slices=None, subset=None):
        """
        Compute a fixed resolution buffer for a component. This should
        ideally work in 1, 2, or 3 dimensions.
        
        If multiple ComponentIDs are passed, a fixed resolution buffer is
        computed for each one.
        
        Parameters
        ----------
        component_id : ComponentID or iterable of component IDs
            The componentID(s) for which to compute a fixed resolution buffer
        slices : iterable
            An iterable giving information about which dimensions we should
            slice along, and which dimensions should be used for the fixed
            resolution buffer. The length of this iterable should be the number
            of dimensions, and for each dimension, either a single value should
            be given (to indicate a slice) or a tuple of (min, max, size)
            should be used to indicate the limits and number of pixels for the
            fixed resolution buffer.
        subset : Subset, optional
            The subset, if applicable. If set, the fixed resolution buffer will
            include only values in the subset.
        
        Examples
        --------
        
        The following example will take a 4-d dataset, will slice it along the
        first and third dimension, and will return a fixed resolution buffer
        with shape (20, 30) along the second and fourth dimensions::
        
            >>> slices = (1.4, (2, 5, 20), 2.2, (1.2, 4.4, 30))
            >>> image = d.compute_frb(d.id['density'], slices=slices)
            >>> image.shape
            (20, 30)
        """
        raise NotImplementedError()
    
    @abstractmethod
    def compute_seq(self, component_id, max_length=None, subset=None):
        """
        Compute a sequence of values for the component.
        
        For datasets that are intrinsically regular and n-dimensional, this can
        be all the values of the data, while for datasets that are less
        structured, this can be a representative set of values.
        
        If multiple ComponentIDs are passed, a sequence is computed for each
        component.
        
        Parameters
        ----------
        component_id : ComponentID or iterable of component IDs
            The componentID(s) for which to compute a sequence
        max_length : int, optional
            The maximum length the sequence(s) can be
        subset : Subset, optional
            The subset, if applicable. If set, the sequence will include only
            values in the subset.
        """
        raise NotImplementedError()
        
        
