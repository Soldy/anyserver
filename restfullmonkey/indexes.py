"""
json indexes class
"""
import os
import json
from copy import deepcopy
from restfullmonkey.indexesabstract import IndexesAbstractClass


class IndexesClass(IndexesAbstractClass):
    """
    Index class.
    :param: logging :
    :param: dict[str,str] :
    """
    def _loadIndex(self):
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
            if path not in self._serials:
                self._serials[path] = 0
            for i in self._index[path]:
                if int(i) > self._serials[path]:
                    self._serials[path] = int(i)

    def check(self)->bool:
        """
        Index cache check

        :return: bool
        """
        index_file = self._config['index']
        _error = False
        if not self._config['load'] and not self._config['save']:
            return False
        if not os.path.exists(index_file):
            self._log.info('Creating index file')
            with open(index_file, 'w') as file_:
                json.dump({}, file_)
        if not os.path.isfile(index_file):
            self._log.critical('Index file error')
            return True
        self._loadIndex()
        return False

    def _saveIndex(self):
        """
        Index cache save
        """
        if not self._config['save']:
            return
        file_name = self._config['index']
        with open(file_name, 'w') as index_file:
            json.dump(self._index, index_file)

    def add(self, path_:str)->str:
        """
        add public function

        :param: str
        :return: str
        """
        before = -1
        if path_ in self._serials:
            before = int(self._serials[path_])
        super().add(path_)
        if before != self._serials[path_]:
            self._saveIndex()
        return str(self._serials[path_])

    def all(self, path_:str)->list[str]:
        """
        all index in path

        :param: str
        :return: list[str]
        """
        if path_ not in self._index:
            return []
        return deepcopy(self._index[path_])
