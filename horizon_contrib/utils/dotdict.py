
class dotdict(dict):

    """ Dictionary with dot access """

    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def list_to_dotdict(array):
    """convert all items in array to dotdict"""

    if isinstance(array, list):
        result = []

        for item in array:
            try:
                _dotdict = dotdict(item)
            except Exception as e:
                raise e
            result.append(_dotdict)

        return result

    return array
