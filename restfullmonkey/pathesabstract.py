"""
pathes apbstract
"""
from copy import deepcopy

class PathesAbstractClass:
    """
    Multipath manager class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(
      self,
      logging_,
      config_
    ):
        self._log    = logging_
        self._config = config_
        self._serial = 0
        self._path = {}
        self._addToCahe('_')

    def check(self)->bool:
        """
        Path dbm check
        :return: bool : False
        """
        if len(self._path) > 0:
            return True
        return False

    def _getFromCache(
      self,
      path_ : str
    )->str:
        """
        get a single path from cache

        :param: str : path_
        :return: str
        """
        return str(self._path[path_])

    def _addToCahe(
      self,
      path_ : str
    )->str:
        """
        add a single path to cache

        :param: str : path_
        :return: str
        """
        if path_ not in self._path:
            self._serial = self._serial + 1
            self. _path[path_] = str(self._serial)
        return str(self._path[path_])

    def get(
      self,
      path_ : str
    )->str:
        """
        add a path

        :param: str : path_
        :return: str
        """
        return self._addToCahe(path_)

    def all(self)->dict[str,str]:
        """
        get all path

        :return: dict[str, str]
        """
        return deepcopy(self._path)
