import yaml


def _add_cache(method):
    """ Add cache to instance method

    New method will try to read value from cache. Otherwise,
    it will compute from scratch using original method

    Warning:
        - Do not use with methods that are dependent on mutable attributes
        - Avoid name space collisions by not picking attribute names that start
            with `cached_`

    Parameters
    ----------
    method : func
        Method to add cache to

    Returns
    -------
    func
        Function with cache

    """
    def _method_with_cache(obj):
        cached_attribute = f'cached_{method.__name__}'

        try:
            return getattr(obj, cached_attribute)
        except AttributeError:
            res = method(obj)
            setattr(obj, cached_attribute, res)
            return res

    return _method_with_cache


class cached_property(property):

    def __init__(self, fget, fset=None, fdel=None, doc=None):
        """ Override of built-in `property` object with modified
        `fget` to cached version

        Parameters
        ----------
        fget : func
            Getter
        fset : func, optional
            Setter
        fdel : func, optional
            Deleter
        doc : str, optional

        """
        if fset is not None:
            raise ValueError('Cannot used `cached_property` on property with setter')

        super().__init__(_add_cache(fget), fset, fdel, doc)


def write_yaml(dict_, file_path):
    """ Write dictionary to file in YAML format

    Parameters
    ----------
    dict_ : dict
    file_path : str

    """
    with open(file_path, 'w') as yaml_file:
        yaml.dump(dict_, yaml_file)
