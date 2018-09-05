import itertools


class PlusEqualsableIterator:
    def __init__(self):
        self._iter = (x for x in [])

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)

    def __iadd__(self, other):
        # import pdb;pdb.set_trace()
        self._iter = itertools.chain(self._iter, [other])
        return self

    def __repr__(self):
        return "<{} at {}>".format(self.__class__.__name__, hex(id(self)))
