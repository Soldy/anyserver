"""
dbm database
"""
import os
import json
"""
We don’t want to support the full DBM, just the GNU. 
NDBM has undocumented limitations that can end in unexpected errors.
GNU works just fine with BSD and with Linux.
If someone using windows that not our problem. 
"""
import dbm.gnu
import traceback
import logging

from typing import Optional, List, Dict, Any

from restfullmonkey.pathesdbm import PathesDbmClass
from restfullmonkey.indexesdbm import IndexesDbmClass
from restfullmonkey.databasehelp import DatabaseHelpClass
from restfullmonkey.databaseabstract import DatabasesAbstractClass

class DatabasesDbmClass(DatabasesAbstractClass):
    """
    database dbm class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(
      self,
      logging_ : logging,
      config_ : dict[str,str]
    ):
        super().__init__(logging_, config_)
        self._indexes : IndexesDbmClass = IndexesDbmClass(
          self._log,
          self._config
        )
        self._patheses : PathesDbmClass = PathesDbmClass(
          self._log,
          self._config
        )
        self.check()

    def _fileName(self, path_: str)->str:
        """
        Dbm path file name
        Yes, that can use a formatted string like :
        ```python
        return os.path.join(
          self._config['dbm_dir'],
          f"{path_}.dbm"
        )
        ```
        But that on the back do a regex.
        That in my view ithis case just wasting
        the cpu time.

        :param: str : the path name
        :return: str: full path 
        """
        return os.path.join(
          self._config['dbm_dir'],
          (self._helper.pathFix(path_)+'.dbm')
        )
    def _dbOpenRead(self, path_:str)->dbm.gnu:
        """
          We try to open the database,
         but if opening fails,
         that probably means the file doesn't exist yet.
          This is  an expected possibility.
         We don't want to create the file for reading 
         if the path doesn't exist yet. 
         Just come back with an empty response. 

         This DB opening method is temporary.
         But for ‘with’ we have to improve the error handling first

        :param: str : the path name
        :return: dbm.gnu:
        """
        db : dbm.gnu | None  = None
        try:
            db = dbm.gnu.open(
              self._fileName(
                path_
              ),
              'r'
            )
        except Exception:
            self._log.error(
              traceback.format_exc()
            )
        return db

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
            db : dbm.gnu = self._dbOpenRead(path_)
            db.close()
            return True
        except Exception:
            return False

    def post(
      self,
      path_ : str,
      data_ : dict[str, str]
    )->int:
        """
        Db record post

        :param: str : the record id in str
        :return: int : result code 0 ok >0 db error
        """
        try:
            """
              We need the cs in here no matter what most of the AI -s said. 
              We close the DB, and if we handle this,
              with 'c' without 's', it can end in data loss.
              DO NOT CHANGE THE ‘cs’ to ‘c’. 
              Can improve the performance but with a price. 
            """
            db : dbm.gnu = dbm.gnu.open(
              self._fileName(
                path_
              ),
              'cs'
            )
        except Exception:
            self._log.error(
              traceback.format_exc()
            )
            return 1
        else:
            _id : str = self._indexes.add(
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

    def __get(self, 
      db_ : dbm.gnu,
      id_ : str
    ):
        return self._helper.outdata(
          json.loads(
            db_.get(
              id_,
              b'{}'
            ).decode("utf-8")
          )
        )

    def getAll(self, path_:str)->list[dict[str,any]]:
        """
        get All record

        :param: str : path
        :return: list[dict[str,any]]
        """
        out = []
        db : dbm.gnu | None = self._dbOpenRead(path_)
        if db is not None:
            key = db.firstkey()
            while key is not None:
                out.append(
                  self.__get(db,key)
                )
                key = db.nextkey(key)
            db.close()
        return out

    def getId(self, 
      path_:str, 
      ids_:list[str]
    )->list[dict[str,any]]:
        """
        get record by Id

        :param: str : path
        :param: str|list[str] : ids
        :return: list[dict[str,any]]
        """
        out : list[dict[str,any]] = []
        db : dbm.gnu | None = self._dbOpenRead(path_)
        if db is not None:
            for i in ids_:
                dat = self.__get(
                  db,
                  str(i)
                )
                if dat != {}:
                    out.append(dat)
            db.close()
        return out

    def getFilter(
      self,
      path_: str,
      filters_: dict[str,str]
    )->list[dict[str,any]]:
        """
        get filter

        :param: str : path
        :param: dict[str,str] : filters
        :return: list[dict[str,any]]
        """
        out : list[dict[str,any]] = []
        """
        Copilot complains that if the filter is a string,
        it should not work properly on the keys.
        Yes, that's true.
        But I never considered this an option to
        this function is called with a string
        because of the type hint.
        In my view, this has no chance.
        But here is some fun for the copilot.
        Let's waste some CPU time.
        But not too much; we don't call an extra try;
        just an if and return and say good bye.
        """
        if isinstance(filters_, str):
            return out
        db : dbm.gnu | None = self._dbOpenRead(path_)
        if db is not None:
            record : dict[str,any] = {}
            key : str = db.firstkey()
            while key is not None:
                record = self.__get(db,key)
                find_it : bool = False
                for filter_key in filters_.keys():
                    if filter_key in record:
                        for filter_val in filters_[filter_key]:
                            if filter_val in record[filter_key]:
                                out.append(record)
                                find_it = True
                                break
                        if find_it is True:
                           break
                key = db.nextkey(key)
            db.close()
        return out
