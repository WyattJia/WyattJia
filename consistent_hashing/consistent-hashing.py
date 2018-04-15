#/usr/bin/env python3

"""
Consistent Hashing demo in Python.
"""

from hashlib import md5
from typing import Dict, List

class Entry:

    _key = ''

    def __init__(self, key):
        self._key = key

    def __str__(self):
        return self._key


class Server:

    _name = ''
    _entries = {}

    def __init__(self, name):
        self._name = name
        # _entries key and value should be Entry type.
        self._entries = {}  # type: Dict[Entry, Entry]

    def put(self, e:Entry) -> None:
        self._entries[e] = e

    def get(self, e:Entry) -> dict:
        return self._entries[e]


class Cluster:

    _SERVER_SIZE_MAX = 1024

    _servers: List[Server] = []
    _size = 0

    @staticmethod
    def string_hashcode(s: str) -> str:
        h = 0
        for c in s:
            h = (31 * h + ord(c)) & 0xFFFFFFFF
        return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

    def put(self, e:Entry) -> None:
        _index = string_hashcode(e) % size
        server = Server(_index)
        server = server.put(e)
        _servers.append(server)    # servers[index].put(e);

    def get(self, e: Entry) -> Entry:
        _index = string_hashcode(e) % size
        for i in _servers:
            # typeof(i) == Server
            if i._name == _index:
                return i.get(e)

    def add_server(self, s:Server) -> bool:
        if _size >= _SERVER_SIZE_MAX:
            return False
        # server = Server(_SERVER_SIZE_MAX)
        # _servers.append(server)
        self._size = _size + 1
        return True


def main():
    pass

if __name__ == "__main__":
    print("Hello world")
