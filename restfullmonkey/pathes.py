"""
Json pathes class
"""
import os
import json
from restfullmonkey.pathesabstract import PathesAbstractClass

class PathesClass(PathesAbstractClass):
    """
    Multipath manager for json store

    :param: logging :
    :param: dict[str,str] :
    """
    def _load(self):
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
            self._serial = max(self._serial, int(self._path[i]))

    def check(self)->bool:
        """
        Path cache check

        :return: bool
        """
        path_file = self._config['path']
        if not self._config['load']:
            return False
        if not os.path.exists(path_file):
            self._log.info('Creating index file')
            with open(
              path_file,
              'w'
            ) as file_:
                json.dump({}, file_)
        if not os.path.isfile(path_file):
            self._log.info('Path file not exist')
            return True
        self._load()
        return False

    def __savePath(self):
        """
        Path cache save
        """
        if not self._config['save']:
            return
        with open(
          self._config['path'],
          'w'
        ) as path_file:
            json.dump(self._path, path_file)

    def add(self, path_:str)->str:
        """
        add / generate a path id

        :param: str : path_
        :return: str
        """
        before = int(self._serial)
        path = super().add(path_)
        if before != self._serial:
            self.__savePath()
        return path
