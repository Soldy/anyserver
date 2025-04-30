from copy import deepcopy 
from sys import argv
import os
import json


"""
Index class.
"""
class IndexesClass:
    def __init__(self, logging_, config_):
        self._log = logging_
        self._config = config_
        self._ids = {}
        self._index = {}

    """
    Index cache load 
    """
    def load(self):
        if not self._config['load']:
            return
        self._log.debug(
          'Loading indexes file'
        )
        with open(self._config['index'], 'r') as file_:
            self._index = json.load(file_)
        for path in self._index:
            if path not in self._ids:
                self._ids[path] = 0
            for i in self._index[path]:
                if int(i) > self._ids[path]:
                    self._ids[path] = int(i)

    """
    Index cache check
    """
    def check(self)->bool:
        _file_ = self._config['index']
        _error = False
        if not self._config['load']:
            return False
        if not self._config['save']:
            return False
        if not os.path.exists(_file_):
            self._log.info('Creating index file')
            with open(_file_, 'w') as file_:
                json.dump({}, file_)
        if not os.path.isfile(_file_):
            self._log.critical('Index file error')
            return True
        self.load()
        return False

    """
    Index cache save
    """
    def save(self):
        if not self._config['save']:
            return
        _file_ = self._config['index']
        with open(self._config['index'], 'w') as file_:
            json.dump(self._index, file_)
    def _addIndex(self, path_:str, id_:str):
        if path_ not in self._index:
            self._index[path_] = []
        if id_ not in self._index[path_]:
            self._index[path_].append(deepcopy(id_))
            self.save()
    def _addId(self, path_:str):
        if path_ not in self._ids:
            self._ids[path_] = 0
        self._ids[path_] = self._ids[path_] + 1
    def add(self, path_:str)->str:
        self._addId(path_)
        self._addIndex(path_, str(self._ids[path_]))
        return str(self._ids[path_])
    def all(self, path_:str):
        if path_ not in self._index:
            return []
        return deepcopy(self._index[path_])
