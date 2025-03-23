from copy import deepcopy 
from sys import argv
import os
import json


class PathesClass:
    def __init__(self, logging_, config_):
        self._log    = logging_
        self._config = config_
        self._serial = 0
        self._path   = {}
    def check(self)->bool:
        _error = False
        if not os.path.exists(
          self._config['path'],
        ):
            self._log.info('Creating index file')
            with open(
              self._config['path'],
              'w'
            ) as file_:
                json.dump({}, file_)
        if not os.path.isfile(
          self._config['path'],
        ):
            self._log.critical('Path file error')
            return True
        return False
     def save(self):
         with open(
           self._config['path'], 
           'w'
         ) as file_:
             json.dump(self._path, file_)

    def read(self):
        with open(
          self._config['path'],
          'r'
        ) as file_:
            self._path = json.load(file_)
    def add(self, path_:str)->int:
        if path_ not in self._path:
            self._serial = deepcopy(
              self._serial + 1
            )
            self. _path[path_] = self._serial
            self.save()
        return self._path[path_]
    def get(path_:str)->int:
        return self.add(path_)
    def all(self):
        return deepcopy(self._path)
