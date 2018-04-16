# /usr/bin/env python3

"""
Consistent Hashing demo in Python.
~ 哈希一致性 Python 语言实现

   ~ 关键抽象
     * Entry 放入 cache 服务器中的对象
     * Server 真正放入缓存对象的 cache 服务器
     * Cluster 服务器集群。（假设会维护一组服务器，这相当于是一组服务器的代理，
       接受  put, get 请求，通过一定算法（普通取余或者哈希一致性将请求转发给特定的 server ）
"""

from hashlib import md5
from typing import Dict, List


class Entry(str):
    _key = ''

    def __init__(self, key):
        super().__init__()
        self._key = key

    def __str__(self):
        return self._key


class Server:
    _name = ''
    _entries = {}

    def __init__(self, name):
        self._name = name
        self._entries: Dict[Entry, Entry] = {}

    def put(self, e: Entry) -> None:
        self._entries[e] = e

    def get(self, e: Entry) -> dict:
        return self._entries.get(e)


class Cluster:
    _SERVER_SIZE_MAX = 1024

    _servers: List[Server] = []
    _size = 0

    def put(self, e: Entry) -> None:
        _index = Cluster.string_hashcode(e) % self._size
        self._servers[_index].put(e)

    @staticmethod
    def string_hashcode(key, encoding='utf-8'):
        m = md5(key.encode(encoding)).hexdigest()
        return int(m, 16)

    def get(self, e: Entry) -> Entry:
        _index = Cluster.string_hashcode(e) % self._size
        return self._servers[_index].get(e)

    def add_server(self, s: Server) -> bool:
        if self._size >= self._SERVER_SIZE_MAX:
            return False
        else:
            self._servers.append(s)
            self._size = self._size + 1
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


def find_entries(c: Cluster, entries: List) -> None:
    for e in entries:
        if e == c.get(e):
            print("重新找到了 entry: {}".format(str(e)))
        else:
            print("entry {} 已失效".format(str(e)))


def main():
    c = create_cluster()
    entries = []
    entry_items = ["i", "have", "a", "pen", "an", "apple", "applepen",
                   "pineapple", "pineapplepen", "PPAP"]

    for item in entry_items:
        entries.append(Entry(item))

    for e in entries:
        c.put(e)

    c.add_server(Server("192.168.0.6"))  # 如果增加一个 Server，大部分 object 都会失效。

    find_entries(c, entries)


if __name__ == "__main__":
    main()
