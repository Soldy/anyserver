"""
dbm indexes
"""
import json
import dbm.gnu
from copy import deepcopy


class IndexesDbmClass:
    """
    Index class.
    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(self, logging_, config_: str):
        self._log    = logging_
        self._config = config_
        self._ids    = {}
        self._index  = {}
        self._db     = dbm.gnu.open(
          self._config['dbm_index'],
          'cs'
        )

    def check(self)->bool:
        """
        Index dbm check
        :return: bool : False
        """
        return False

    def get(self, path_:str)->dict[str,int|list[str]]:
        """
        get an index id in the path

        :param: str : path_
        :return: dict[str,int|list[str]]
        """
        return json.loads(
          self._db.get(
            path_,
            b'{"serial":0,"index":[]}'
          ).decode("utf-8")
        )

    def add(self, path_:str)->str:
        """
        add an index id to the path

        :param: str : path_
        :return: str
        """
        current = self.get(path_)
        current['serial'] = current['serial'] + 1
        current['index'].append(
          str(current['serial'])
        )
        self._db[path_] = json.dumps(current)
        return str(current['serial'])

    def all(self, path_:str):
        """
        get all indexes

        :param: str : path_
        :return: str
        """
        return deepcopy(self.get(path_)['index'])
