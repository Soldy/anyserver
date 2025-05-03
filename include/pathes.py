"""
Json pathes class
"""
import os
import json
from copy import deepcopy

class PathesClass:
    """
    Multipath manager class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(
      self,
      logging_,
      config_: dict[str,str]
    ):
        self._log    = logging_
        self._config = config_
        self._serial = 0
        self._path   = {}

    def load(self):
        """
        Path cache load 
        """
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
                self._serial = int(self._path[i])

    def check(self)->bool:
        """
        Path cache check
        """
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
        self.load()
        return False

    def save(self):
        """
        Path cache save
        """
        if not self._config['save']:
            return
        with open(
          self._config['path'],
          'w'
        ) as file_:
            json.dump(self._path, file_)

    def add(self, path_:str)->str:
        """
        add / generate a path id

        :param: str : path_
        :return: str
        """
        if path_ not in self._path:
            self._serial = self._serial + 1
            self. _path[path_] = deepcopy(self._serial)
            self.save()
        return deepcopy(str(self._path[path_]))

    def get(self, path_:str)->str:
        """
        get a path id

        :param: str : path_
        :return: str
        """
        return self.add(path_)

    def all(self):
        """
        get all path

        :param: str : path_
        :return: str
        """
        return deepcopy(self._path)
