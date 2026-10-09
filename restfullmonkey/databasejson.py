"""
json database
"""
import os
import sys
import csv
import json
import logging

from copy import deepcopy

from restfullmonkey.pathesjson import PathesClass
from restfullmonkey.indexesjson import IndexesClass
from restfullmonkey.databaseabstract import DatabasesAbstractClass


class DatabasesJsonClass(DatabasesAbstractClass):
    """
    database json class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(
      self,
      logging_ : logging,
      config_ : dict[str,str]
    ):
        super().__init__(logging_, config_)
        self._db = {}
        self._indexes = IndexesClass(
          self._log,
          self._config
        )
        self._patheses = PathesClass(
          self._log,
          self._config
        )
        self.check()
        self.loadAll()

    def _checkDir(self):
        """
        check dir existance
        """
        if (not self._config['save'] and
          not self._config['load']):
            return False
        return self._helper.checkDir(
          self._config["db_dir"]
        )

    def check(self):
        """
         This checking the file system
         for initialization.
        """
        _error = False
        if self._checkDir():
            _error = True
        if self._patheses.check():
            _error = True
        if self._indexes.check():
            _error = True
        if _error :
            sys.exit()

    def checkPath(self, path_:str)->bool:
        """
         Checking path in db

         :param: str:
         :return: bool:
        """
        path = self._patheses.get(path_)
        if path not in self._db:
            return False
        return True

    def _fileName(
      self,
      path_: str,
      id_: str
    )->str:
        """
        Db record file name 

        :param: str : the path name
        :param: str : the record id in str
        :return: str: full path
        """
        return os.path.join(
          self._config["db_dir"],
          (path_+'_'+str(id_)+'.json')
        )

    def load(self, path_: str, id_: str):
        """
        Db record load

        :param: str : the record id in str
        """
        if not self._config["load"]:
            return
        if path_ not in self._db:
            self._db[path_] = {}
        with open(self._fileName(path_, id_), 'r') as file_:
            self._db[path_][id_] = json.load(file_)
    def loadAll(self):
        """
        load all db records

        :param: dict[str, dict[str, str]] index
        """
        self._log.debug(
           'Loading Database'
        )
        for path in self._patheses.all():
            path = self._patheses.get(
              path
            )
            for id_ in self._indexes.all(
              path
            ):
                self.load(path, id_)

    def save(self, path_: str, id_:str):
        """
        Db record save

        :param: str : the record id in str
        """
        if self._config['save'] is True:
            with open(
              self._fileName(path_, id_),
              'w'
            ) as file_:
                json.dump(self._db[path_][id_], file_)

    def _set(
      self,
      path_: str,
      id_: str,
      data_: dict[str,any]
    ):
        """
        set record value

        :param: str : the record path
        :param: str : the record id in str
        :param: dict[str,any] : data
        """
        if path_ not in self._db :
            self._db[path_] = {}
        self._db[path_][id_] = {}
        self._db[path_][id_]['data'] = deepcopy(data_)
        self._db[path_][id_]['id'] = deepcopy(id_)
        self.save(path_, id_)

    def post(
      self,
      path_: str,
      data_: dict[str, str]
    )->int:
        """
        Db record post

        :param: str : the record id in str
        :param: dict[str, str] : record data
        :return: int : result code 0 ok
        """
        path = self._patheses.get(
          self._helper.pathFix(path_)
        )
        _id = self._indexes.add(
          self._patheses.get(
            self._helper.pathFix(path_)
          )
        )
        self._set(path, _id, data_)
        return 0

    def patch(
      self,
      path_: str,
      data_: dict[str, str]
    )->int:
        """
        Db record post
         result codes:
            0 - O.K.
            1 - missing id (invalid request)
            2 - unkown path 
            3 - unkown id

        :param: str : the record id in str
        :return: int : result code 0 ok
        """
        path = self._patheses.get(
          self._helper.pathFix(path_)
        )
        if 'id' not in data_:
            return 1
        _id = data_['id']
        if path not in self._db:
            return 2
        if _id not in self._db[path]:
            return 3
        self._set(path, data_['id'], data_)
        return 0

    def _getCopy(
      self,
      path_:str,
      ids_:list[str]
    )->list[dict[str,any]]:
        """
        get result element copy

        :param:  str : element path
        :param:  list[str] : element list
        :return: list[dict[str,any]] : result element copy
        """
        out = []
        db_path = self._db.get(path_, {})
        for i in ids_:
            if i in db_path:
                out.append(self._helper.outdata(db_path[i]))
        return out

    def getAll(self, path_:str):
        """
        get All record

        :param: str : path
        :return: dict[str,any]
        """
        path = self._patheses.get(path_)
        return self._getCopy(
          path,
          self._db[
            path
          ].keys()
        )

    def getId(self, path_: str, ids_: list[str]):
        """
        get records by id

        :param: str : path
        :param: list[str] : id list
        :return: dict[str,any]
        """
        path = self._patheses.get(path_)
        out = []
        for i in ids_:
            if str(i) in self._db[path]:
                out.append(str(i))
        return self._getCopy(path, out)

    def getFilter(
      self,
      path_: str,
      filters_: dict[str,str]
    ):
        """
        get elements by filter

        :param: str : path
        :param: dict[str,str] : filters
        :return: dict[str,any]
        """
        out = []
        path = self._patheses.get(path_)
        for row in self._db[path]:
            if self.filterCheck(
               self._db[path][row]['data'],
               filters_
            ):
                out.append(str(row))
        return self._getCopy(path, out)

    def columns(
      self,
      path_:str,
      migration_ : bool = False
    )->dict[str,dict[str, int|list[str]]]:
        """

        :param: str :  path name 
        :param: bool
        :return: dict[str,dict[str, int|list[str]]] :
        """
        path = self._patheses.get(
          self._helper.pathFix(path_)
        )
        out = {}
        if path not in self._db:
            return out
        for i in self._db[path]:
            row = {}
            if migration_ is True:
                row = self._migrationRowFix(
                  self._db[path][i]['data']
                )
            else:
                row = self._db[path][i]['data']
            row[self._config['id_name']] = i
            out = self.columDetails(
              out,
              row
            )
        return out

    def columnShow(
        self,
        path_:str,
        column_:str
    )->dict[str,any]:
        """

        :param: str :  path name
        :param: str :  column name
        :return: dict[str, any] :
        """
        path = self._patheses.get(
          self._helper.pathFix(path_)
        )
        out = {}
        if path not in self._db:
            return out
        for i in self._db[path]:
            if column_ in self._db[path][i]['data']:
                out[str(i)] = self._db[path][i]['data'][column_]
        return out

    def count(self, path_:str)->int:
        """

        :param: str :  path name 
        :return: int : count records in path
        """
        path = self._patheses.get(
          self._helper.pathFix(path_)
        )
        if path in self._db:
            return len(self._db[path].keys())
        return 0


    def countAll(self)->dict[str,int]:
        """
        :return: int : count all records
        """
        out = {}
        for a in self._patheses.all():
            out[a] =  self.count(a)
        return out

    def migrationToCsv(
      self,
      path_ : str,
      output_file_ : str
    )->bool:
        """

        :param: str
        :param: str
        :return: bool
        """
        path = self._patheses.get(
          self._helper.pathFix(path_)
        )
        if path not in self._db:
            return False
        file_name = output_file_+'.csv'
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
              csvfile,
              fieldnames=(
                self.columns(path_,True)
              )
            )
            writer.writeheader()
            for i in self._db[path]:
                writer.writerow(
                  self._migrationRowFix(
                    self._db[path][i]['data']
                  )
                )
            return True
        return False
