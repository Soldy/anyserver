import os
import json
import dbm.gnu
from sys import argv
from copy import deepcopy 


"""
Multipath manager class.
"""
class PathesDbmClass:
    def __init__(self, logging_, config_):
        self._log    = logging_
        self._config = config_
        self._serial = 0
        self._db     = dbm.gnu.open(
          self._config['dbm_path'],
          'cs'
        )
    """
    Path dbm check
    :return: bool : False
    """
    def check(self)->bool:
        return False

    """
    temp dummy save
    """
    def save(self):
        return

    """
    temp dummy load 
    """
    def load(self):
        return 

    """
    get a path id

    :param: str : path_
    :return: str
    """
    def get(self, path_:str)->str:
        return str(int(
          self._db.get(path_, b'-1').decode("utf-8")
        ))

    """
    add / generate a path id

    :param: str : path_
    :return: str
    """
    def add(self, path_:str)->str:
        if self.get(path_) == '-1':
            self._serial = self._serial + 1
            self._db[path_] = str(self._serial)
        return self.get(path_)

    """
    get all path

    :param: str : path_
    :return: str
    """
    def all(self):
        out = {}
        key = self._db.firstkey()
        while key is not None:
          out[key.decode('utf-8')] = self._db[key].decode('utf-8')
          key = self._db.nextkey(key)
        return out
