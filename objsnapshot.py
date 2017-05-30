from copy import deepcopy
from datetime import datetime


class Commit(object):
    """
    Commit of object state.

    """
    def __init__(self, state, uses_slots=False):
        """
        @param state dict: object state.
        @param uses_slots bool = False: indicator of the usage of slots attribute.

        """
        self._ctime = datetime.now()
        self._state = state
        self._uses_slots = uses_slots

    @property
    def creation_time(self):
        return self._ctime

    @property
    def uses_slots(self):
        return self._uses_slots

    @property
    def state(self):
        return self._state

    def __str__(self):
        return "Commit <{} {}>".format(self._state, self._uses_slots)

def commit(obj):
    """
    Commit object state.

    @param obj object: python object.

    @returns Commit object.
    """
    if hasattr(obj, "__dict__"):
        return Commit(deepcopy(obj.__dict__))
    elif hasattr(obj, "__slots__"):
        return Commit(state={x:getattr(obj, x) for x in obj.__slots__}, uses_slots=True)
    else:
        raise ValueError("obj {} doesn't have `__dict__` or `__slots__` attributes to commit.")

def rollback(obj, commit):
    """
    Rollback an object to a certain state.

    @param obj object: python object to restore it's state.
    @param commit Commit: used to restore obj to that commit.

    @returns obj at earlier version commit
    """
    copy = deepcopy(obj)
    if commit.uses_slots is False:
        copy.__dict__ = commit.state
    else:
        for k, v in commit.state.items():
            setattr(copy, k, v)

    return copy


