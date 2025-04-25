from copy import deepcopy 
from sys import argv
import os
import json


"""
Multipath manager class.
"""
class PathesClass:
    def __init__(self, logging_, config_):
        self._log    = logging_
        self._config = config_
        self._serial = 0
        self._path   = {}

    """
    Path cache check
    """
    def check(self)->bool:
        _file_ = self._config['path']
        _error = False
        if not self._config['load']:
            return False
        if not self._config['save']:
            return False
        if not os.path.exists(_file_):
            self._log.info('Creating index file')
            with open(
              _file_,
              'w'
            ) as file_:
                json.dump({}, file_)
        if not os.path.isfile(_file_):
            self._log.critical('Path file error')
            return True
        return False

    """
    Path cache save
    """
    def save(self):
        if not self._config['save']:
            return
        with open(
          self._config['path'],
          'w'
        ) as file_:
           json.dump(self._path, file_)

    """
    Path cache load 
    """
    def load(self):
        if not self._config['load']:
            return
        self._log.debug(
          'Loading patheses file'
        )
        with open(
          self._config['path'],
          'r'
        ) as file_:
            self._path = json.load(file_)
        for i in self._path:
            if int(self._path[i]) >= self._serial:
               self._serial = int(self._path[i]) + 1
    def add(self, path_:str)->str:
        if path_ not in self._path:
            self._serial = self._serial + 1
            self. _path[path_] = deepcopy(self._serial)
            self.save()
        return deepcopy(str(self._path[path_]))
    def get(self, path_:str)->str:
        return self.add(path_)
    def all(self):
        return deepcopy(self._path)
