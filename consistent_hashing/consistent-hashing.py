#/usr/bin/env python3

"""
Consistent Hashing demo in Python.
~ 哈希一致性 Python 语言实现

   ~ 关键抽象
     * Entry 放入 cache 服务器中的对象
     * Server 真正放入缓存对象的 cache 服务器
     * Cluster 服务器集群。（假设会维护一组服务器，这相当于是一组服务器的代理，接受  put, get 请求，通过一定算法（普通取余或者哈希一致性将请求转发给特定的 server ）
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
        for i in _servers:
            # typeof(i) == Server
            if i._name == _index:
                i.put(e)

    def get(self, e: Entry) -> Entry:
        _index = string_hashcode(e) % size
        for i in _servers:
            # typeof(i) == Server
            if i._name == _index:
                return i.get(e)

    def add_server(self, s:Server) -> bool:
        if _size >= _SERVER_SIZE_MAX or len(_servers) >= _SERVER_SIZE_MAX:
            return False
        elif len(_servers) < _SERVER_SIZE_MAX:
            _servers.append(server)
            self._size = _size + 1
            return True


def create_cluster():
    c = Cluster()
    c.add_server(Server("192.168.0.0"))
    c.add_server(Server("192.168.0.1"))
    c.add_server(Server("192.168.0.2"))
    c.add_server(Server("192.168.0.3"))
    c.add_server(Server("192.168.0.4"))
    c.add_server(Server("192.168.0.5"))
    return c


def find_entries(c: Cluster, entries: List) -> Str:
    for e in entries:
        if e == c.get(e):
            return '重新找到了 entry: {}'.format(str(e))
        else:
            return "entry {} 已失效".format(str(e))


def main():
    c = create_cluster()
    entries = []
    entry_items = ["i", "have", "a", "pen", "an", "apple",  "applepen",
                   "pineapple", "pineapplepen", "PPAP"]

    for item in entry_items:
        entries.append(Entry(item))

    for e in entries:
        c.put(e)

    c.add_server(Server("192.168.0.6"))

    find_entries(c, entries)


if __name__ == "__main__":
    main()

