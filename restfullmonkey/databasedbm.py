"""
dbm database
"""
import json
import dbm.gnu
from pathesdbm import PathesDbmClass
from indexesdbm import IndexesDbmClass
from databasehelp import DatabaseHelpClass

class DatabasesDbmClass:
    """
    database dbm class

    :param: logging :
    :param: dict[str,str] :
    """
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

    def _fileName(self, path_: str)->str:
        """
        Dbm path file name

        :param: str : the path name
        :return: str: full path 
        """
        return (
          self._config["dbm_dir"]+
          '/'+
          path_+
          '.dbm'
        )

    def check(self):
        """
         Checking the file system
         for initialization.
        """
        return self._helper.checkDir(
          self._config["dbm_dir"]
        )

    def checkPath(self, path_:str)->bool:
        """
         Checking path.dbm in dbdir

         :param: str:
         :return: bool:
        """
        try:
            db = dbm.gnu.open(
              self._fileName(
                path_
              ),
              'r'
            )
            db.close()
            return True
        except Exception:
            return False

    def post(self,
      path_: str,
      data_: dict[str, str]
    )->int:
        """
        Db record post

        :param: str : the record id in str
        :return: int : result code 0 ok
        """
        path = self._helper.pathFix(path_)
        db = dbm.gnu.open(
          self._fileName(
            path
          ),
          'cs'
        )
        _id = self._indexes.add(
          self._patheses.add(
            path_
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

    def __get(self, db_, id_):
        return self._helper.outdata(
          json.loads(
            db_.get(
              id_,
              b'{}'
            ).decode("utf-8")
          )
        )

    def getAll(self, path_:str):
        """
        get All record

        :param: str : path
        """
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
              self.__get(db,key)
            )
            key = db.nextkey(key)
        db.close()
        return out

    def getId(self, path_:str, ids_:list[str]):
        """
        get All record

        :param: str : path
        """
        try:
            out = []
            db = dbm.gnu.open(
              self._fileName(
                path_
              ),
              'r'
            )
            for i in ids_:
                dat = self.__get(
                  db,
                  str(i)
                )
                if dat != {}:
                    out.append(dat)
            db.close()
            return out
        except Exception:
            return []

    def getFilter(
      self,
      path_: str,
      filters_: dict[str,str]
    ):
        """
        get filter

        :param: str : path
        :param: dict[str,str] : filters
        """
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
            a = self.__get(db,key)
            for b in filters_:
                if b in a:
                    for c in filters_[b]:
                        if c in a[b]:
                            out.append(a)
            key = db.nextkey(key)
        db.close()
        return out
