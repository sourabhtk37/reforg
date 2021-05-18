__version__ = "0.1"
__author__ = "T K Sourab <sourabhtk37@gmail.com>"

from collections import OrderedDict

import logging
import logging.config
import dbm

ENCODING = "utf-8"

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


class KvStore:
    """KeyValue store implementing LRU cache and persistent storage with dbm

    Implements an OrderedDict(which is bascially doublyLinkedList) with
    hashmap/dict that clears/pop the least recently used key from the cache.

    Usage:
    >>> from kvstore.core import KvStore
    >>> kv_store = KvStore(capacity=100)
    >>> kv_store.put("a","b")
    >>> kv_store.get("a")
    'b'
    >>> kv_store.put("c","d")
    >>> kv_store.get("c")
    'd'

    :attr capacity: LRU cache size, default=999
    """

    def __init__(self, capacity: int = 999):
        """Creates an OrderedDict of the specified capacity"""
        self.__cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> str:
        """Retreives key from cache/dbm

        Recently used keys are moved to front of the OrderedDict.
        If keys not present in cache, it is then checked in dbm.
        Error is logged if key is not found in dbm.

        :params key: key to fetch from cache/dbm
        :returns str: value corresponding to the key
        """
        if key not in self.__cache:
            # Read from db
            with dbm.open("store_perm", "cs") as db:
                if key in db:
                    self.__cache[key] = db[key]
                    self.__cache.move_to_end(key)
                    return str(self.__cache[key], encoding=ENCODING)

            logger.error("Key or DB not found")
        else:
            self.__cache.move_to_end(key)
            return self.__cache[key]

    def put(self, key: str, value: str) -> int:
        """
        On updates the key is saved to dbm and cache is updated
        and moved to the end. If capacity of LRU cache is exceeded then
        the least recently used key is popped from the cache.

        :params key: key to fetch from cache/dbm
        :params value: value to be updated to the key
        :returns None:
        """

        with dbm.open("store_perm", "cs") as db:
            try:
                db[key] = value
            except TypeError as err:
                logger.error("Invalid type passed")
                return -1
        self.__cache[key] = value
        self.__cache.move_to_end(key)

        if len(self.__cache) > self.capacity:
            self.__cache.popitem(last=False)
