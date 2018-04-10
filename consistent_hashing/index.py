#/usr/bin/env python

"""
Consistent Hashing demo in Python.
"""

class Entry:

    _key = ''

    def __init__(self, key):
        self._key = key

    def __str__(self):
        return self._key


if __name__ == "__main__":
    e = Entry('a')
    print(e)
