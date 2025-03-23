from copy import deepcopy 
from sys import argv
import os
import json


class IndexesClass:
    def __init__(self, logging_, config_):
        self._log = logging_
        self._config = config_
        self._ids = {}
        self._index = {}
    def check(self)->bool:
        _file_ = self._config['index']
        _error = False
        if not os.path.exists(_file_):
            self._log.info('Creating index file')
            with open(_file_, 'w') as file_:
                json.dump({}, file_)
        if not os.path.isfile(_file_):
            self._log.critical('Index file error')
            return True
        return False
    def save(self):
        _file_ = self._config['index']
        with open(self._config['index'], 'w') as file_:
            json.dump(self._index, file_)
    def read(self):
        with open(self._config['index'], 'r') as file_:
            self._index = json.load(file_)

    def add(self, path_:str, id_:str)->int:
        if path_ not in self._index:
            self._index[path_] = []
        if id_ not in self._index:
            self._index[path_].append(deepcopy(id_))
            self.save()
    def addId(self, path:str)->str:
        if path_ not in self._ids:
            self_ids[path_] = 0
        self._ids[path_] = self._ids[path_] + 1
        return deepcopy(str(self._ids[path_]))
    def all(self):
        return deepcopy(self._index)
