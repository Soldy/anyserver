from copy import deepcopy 
from sys import argv
import os
import json


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
            b'{serial:0,index:[]}'
          ).decode("utf-8")
        )

    def add(self, path_:str, id_:str):
        if (self.get(path_))['serial'] == 0:
            self._db[path_] = json.dumps({'serial':0,'index':[]})
        current = self.get(path_)
        if id_ not in current.index:
            current.ids.append(deepcopy(id_))
        self._db[path_] = json.dumps(current)

    def addId(self, path_:str)->str:
        current = self.get(path_)
        current['serial'] = current['serial'] + 1
        self._db[path_] = json.dumps(current)
        return deepcopy(str(
        (self.get(path_))['serial'] == 0:

        ))
    """
    get all indexes

    :param: str : path_
    :return: str
    """
    def all(self, path_:str):
        out = {}
        key = db.firstkey()
        while key is not None
          out[key.decode('utf-8')] = db[key].decode('utf-8')
          key = self_.db.nextkey(key)
        return out
