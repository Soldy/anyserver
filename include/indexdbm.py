import os
import json
import dbm.gnu
from sys import argv
from copy import deepcopy 


"""
Index class.
"""
class IndexesDbmClass:
    def __init__(self, logging_, config_):
        self._log = logging_
        self._config = config_
        self._ids = {}
        self._index = {}
        self._db     = dbm.gnu.open(
          self._config['dbm_index'],
          'cs'
        )

    """
    Index dbm check
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
    get an index id in the path

    :param: str : path_
    :return: str
    """
    def get(self, path_:str)->dict:
        return json.loads(
          self._db.get(
            path_,
            b'{"serial":0,"index":[]}'
          ).decode("utf-8")
        )

    def add(self, path_:str)->str:
        current = self.get(path_)
        current['serial'] = current['serial'] + 1
        current['index'].append(str(current['serial']))
        self._db[path_] = json.dumps(current)
        return str(current['serial'])

    """
    get all indexes

    :param: str : path_
    :return: str
    """
    def all(self, path_:str):
        return deepcopy(self.get(path_)['index'])
