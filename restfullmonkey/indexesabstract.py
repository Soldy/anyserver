"""
dbm indexes abstract
"""
from copy import deepcopy

class IndexesAbstractClass:
    """
    Index class.
    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(self, logging_, config_: str):
        self._log    = logging_
        self._config = config_
        self._serials    = {}
        self._index  = {}

    def _addIndex(self, path_:str, id_:str):
        """
        add new index

        :param: str
        :param: str
        """
        if path_ not in self._index:
            self._index[path_] = []
        if id_ not in self._index[path_]:
            self._index[path_].append(deepcopy(id_))

    def _addId(
      self,
      path_:str
    )->int:
        """
        add new id

        :param: str
        """
        if path_ not in self._serials:
            self._serials[path_] = 0
        self._serials[path_] = self._serials[path_] + 1
        return int(self._serials[path_])

    def get(self, path_:str)->dict[str,int|list[str]]:
        """
        get an index id in the path

        :param: str : path_
        :return: dict[str,int|list[str]]
        """
        if path_ in self._index:
            return {
              'serial' : 0,
              'index'  : []
            }
        return {
          'serial' : int(self._serials[path_]),
          'index'  : deepcopy(self._index[path_])

        }
