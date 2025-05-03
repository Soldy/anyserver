"""
json indexes class
"""
import os
import json
from copy import deepcopy


class IndexesClass:
    """
    Index class.
    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(self, logging_, config_):
        self._log = logging_
        self._config = config_
        self._ids = {}
        self._index = {}

    def load(self):
        """
        Index cache load
        """
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

    def check(self)->bool:
        """
        Index cache check

        :return: bool
        """
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

    def save(self):
        """
        Index cache save
        """
        if not self._config['save']:
            return
        file_name = self._config['index']
        with open(file_name, 'w') as file_data:
            json.dump(self._index, file_data)

    def __addIndex(self, path_:str, id_:str):
        """
        add new index 

        :param: str
        :param: str
        """
        if path_ not in self._index:
            self._index[path_] = []
        if id_ not in self._index[path_]:
            self._index[path_].append(deepcopy(id_))
            self.save()

    def __addId(self, path_:str):
        """
        add new id

        :param: str
        """
        if path_ not in self._ids:
            self._ids[path_] = 0
        self._ids[path_] = self._ids[path_] + 1

    def add(self, path_:str)->str:
        """
        add public function

        :param: str
        :return: str
        """
        self.__addId(path_)
        self.__addIndex(path_, str(self._ids[path_]))
        return str(self._ids[path_])

    def all(self, path_:str)->list[str]:
        """
        all index in path

        :param: str
        :return: list[str]
        """
        if path_ not in self._index:
            return []
        return deepcopy(self._index[path_])
