import os
import json
import pathes
import dbm.gnu
from copy import deepcopy 
from pathesdbm import PathesDbmClass
from indexesdbm import IndexesDbmClass
from databasehelp import DatabaseHelpClass

class DatabasesDbmClass:
    def __init__(self, logging_, config_):
        self._log     = logging_
        self._config  = config_
        self._checked = False
        self._indexes = IndexesDbmClass(
          self._log,
          self._config
        )
        self._patheses = PathesDbmClass(
          self._log,
          self._config
        )
        self._helper = DatabaseHelpClass(
          self._log
        )
        self.check()

    """
    Dbm path file name

    :param: str : the path name
    :return: str: full path 
    """
    def _fileName(self, path_: str)->str:
        return (
          self._config["dbm_dir"]+
          '/'+
          path_+
          '.dbm'
        )

    """
     Checking the file system
     for initialization.
    """
    def check(self):
        return self._helper.checkDir(
          self._config["dbm_dir"]
        )

    """
    Db record post

    :param: str : the record id in str
    :return: int : result code 0 ok
    """
    def post(self,
      path_: str,
      data_: dict[str, str]
    )->int:
        path = self._helper.pathFix(path_)
        db = dbm.gnu.open(
          self._fileName(
            path
          ),
          'cs'
        )
        _id = self._indexes.add(
          self._patheses.get(
            path
          )
        )
        db[_id] = json.dumps(
          self._helper.create(
            _id,
            data_
          )
        )
        db.close()
        return 0

    def _get(self, db_, id_):
        return self._helper.outdata(
          json.loads(
            db_.get(
              id_,
              b'{}'
            ).decode("utf-8")
          )
        )

    """
    get All record

    :param: str : path
    """
    def _getAll(self, path_:str):
        try:
            db = dbm.gnu.open(
              self._fileName(
                path_
              ),
              'r'
            )
        except Exception:
            return {}
        out = []
        key = db.firstkey()
        while key is not None:
            out.append(
              self._get(db,key)
            )
            key = db.nextkey(key)
        db.close()
        return out
    """
    get All record

    :param: str : path
    """
    def _getId(self, path_, id_:str):
        try:
            db = dbm.gnu.open(
              self._fileName(
                path_
              ),
              'r'
            )
            out = self._get(
              db,
              id_
            )
            db.close()
            if out == {}:
                return []
            return [out]
        except Exception:
            return []

    """
    get filter

    :param: str : path
    """
    def _getFilter(
      self,
      path_: str,
      filters_: dict[str,str]
    ):
        try:
            db = dbm.gnu.open(
              self._fileName(
                path_
              ),
              'r'
            )
        except Exception:
            return {}
        out = []
        a = {}
        key = db.firstkey()
        while key is not None:
            a = self._get(db,key)
            for b in filters_:
                if b in a:
                   for c in filters_[b]:
                       if c in a[b]:
                           out.append(a)
            key = db.nextkey(key)
        db.close()
        return out
    """
    get request manager

    :param: str : the record id in str
    """
    def get(
      self,
      path_: str,
      gets_: dict[str,str]
    ):
        path = self._helper.pathFix(path_)
        if 'id' in gets_:
            return self._getId(path, gets_['id'])
        if gets_ == {}:
            return self._getAll(path)
        else:
            return self._getFilter(path, gets_)


