from copy import deepcopy 
from sys import argv
import os
import json
import pathes
import indexes
import logging

_config = {
    "db_dir" : "db",
    "index"  : "indexes.json",
    "path"   : "pathes.json",
    "load"   : True,
    "save"   : True
}

indexes._config = _config
pathes._config = _config

class DatabasesClass:
    def __init__(self, logging_, config_):
        self._log = logging_
        self._config = config_
        self._db = {}
        self._indexes = indexes.IndexesClass(
          self._log,
          self._config
        )
        self._patheses = pathes.PathesClass(
          self._log,
          self._config
        )
    """ This checking the file system for initialization. """
    def check():
        if not self._config["save"] and
           not self._config["load"]:
            return 
        if not os.path.exists(
          self._config["db_dir"]
        ):
            self._log.info(
              'Creating database directory'
            )
            os.makedirs(
              self._config["db_dir"]
            )
        if not os.path.isdir(
          self._config["db_dir"]
        ):
            self._log.critical(
              'Database directory error'
            )
            _error = True
        if _error or
          self._indexes.check() or 
          self._pathes.check():
            quit()
    """
    Db record file name 

    :param: str : the record id in str
    :return: str: full path 
    """
    def fileName(path_: str, id_: str)->str:
        return (
          slef._config["db_dir"]+
          '/'+
          path_+
          '_'+
          str(id_)+
          '.json'
        )
    """
    Db record load

    :param: str : the record id in str
    """
    def load(path_: str, id_: str):
        if self._config["load"] == True:
            if path_ not in self._db:
                self._db[path_] = {}
            with open(self._fileName(path_, id_), 'r') as file_:
                self._db[path_][id_] = json.load(file_)
    """
    load all db records

    :param: dict[str, dict[str, str]] index
    """
    def loadAll(index_: dict[str, dict[str, str]]):
        index =  self._indexes.all()
        for path in index:
            for id_ in index[path]:
                self.load(path, id_)
    """
    Db record save

    :param: str : the record id in str
    """
    def save(path_: str, id_:str):
        if _save_ == True:
            with open(_fileName(path_, id_), 'w') as file_:
                json.dump(self._db[path_][id_], file_)

    """
    Db record post

    :param: str : the record id in str
    """
    def post(path_: str, data_: dict[str, str]):
        _id = self._indexes.addId(
          self._patheses.get(
            _path
          )
        )
        self._db[_id] = {}
        data_['id'] = _id
        self._db[path_][_id]['data'] = deepcopy(data_)
        self._indexes.add(_path, _id)
        self.save()

    """
    Db record save

    :param: str : the record id in str
    """
    def _getCopy(self, path_:str, ids_:list[str]):
        out = []
        for i in ids_:
            if self._db[i]:
                pack = deepcopy(self._db[path_][i]['data'])
                pack['id'] = deepcopy(self._db[path_][i]['id'])
                out.append(deepcopy(pack)
        return out
    """
    get All record

    :param: str : the record id in str
    """
    def _getAll(self, path_:str):
        return self._getCopy(
          path_,
          self._db[
            path_
          ]
        )
    def _getId(self, path_: str, ids_: list[str]):
        out = []
        for i in ids_:
            if str(i) in self._db[path_]:
                out.append(str(i))
        return self._getCopy(path_, out)
    def _getFilter(self, path_: str, filters_: dict[str,str]):
        out = []
        for a in self._db[path_]:
            for b in filters_:
                if b in self._db[path_][a]['data']:
                   for c in filters_[b]:
                       if c in self._db[path_][a]['data'][b]:
                            out.append(str(a))
        return self._getCopy(path_, out)
    def get(path_: str, gets_: dict[str,str]):
        path = self._patheses.get(
          path_
        )
        if path not in self._db[path]:
            return {}
        if 'id' in gets_:
            return self._getId(path, gets_['id']))
        if gets == {}:
            return self._getAll(path)
        else:
            return self._getFilter(path, gets_)


