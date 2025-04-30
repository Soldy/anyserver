from copy import deepcopy 
from sys import argv
import os
import json
import pathes
import indexes
import time


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
        self.check()
        self._patheses.load()
        self._indexes.load()
        self.loadAll()
    """
    path name fix
    """
    def _pathFix(self, path_:str)->str:
        return path_.replace("/", "_")
    def _checkDir(self):
        if not self._config["save"]:
            return False
        if not self._config["load"]:
            return False
        if not os.path.exists(
          self._config["db_dir"]
        ):
            self._log.debug(
              'Creating database directory'
            )
            os.makedirs(
              self._config["db_dir"]
            )
            time.sleep(1)
        if not os.path.isdir(
          self._config["db_dir"]
        ):
            self._log.critical(
              'Database directory error'
            )
            return True
        return False
    """ This checking the file system for initialization. """
    def check(self):
        _error = False
        if self._checkDir():
            _error = True
        if self._patheses.check():
            _error = True
        if self._indexes.check():
            _error = True
        if _error :
            quit()

    """
    Db record file name 

    :param: str : the record id in str
    :return: str: full path 
    """
    def _fileName(self, path_: str, id_: str)->str:
        return (
          self._config["db_dir"]+
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
    def load(self, path_: str, id_: str):
        if not self._config["load"]:
            return
        if path_ not in self._db:
            self._db[path_] = {}
        with open(self._fileName(path_, id_), 'r') as file_:
            self._db[path_][id_] = json.load(file_)
    """
    load all db records

    :param: dict[str, dict[str, str]] index
    """
    def loadAll(self):
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
    """
    Db record save

    :param: str : the record id in str
    """
    def save(self, path_: str, id_:str):
        if self._config['save'] == True:
            with open(
              self._fileName(path_, id_),
              'w'
            ) as file_:
                json.dump(self._db[path_][id_], file_)
    """
    set record value

    :param: str : the record path
    :param: str : the record id in str
    :param: dict[str,any] : data
    """
    def _set(self, path_: str, id_: str, data_: dict[str,any]):
        if path_ not in self._db :
            self._db[path_] = {}
        self._db[path_][id_] = {}
        data_['id'] = deepcopy(id_)
        self._db[path_][id_]['data'] = deepcopy(data_)
        self._db[path_][id_]['id'] = deepcopy(id_)
        self.save(path_, id_)

    """
    Db record post

    :param: str : the record id in str
    :return: int : result code 0 ok
    """
    def post(self, path_: str, data_: dict[str, str])->int:
        path = self._patheses.get(
          self._pathFix(path_)
        )
        _id = self._indexes.add(
          self._patheses.get(
            self._pathFix(path_)
          )
        )
        self._set(path, _id, data_)
        return 0

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
    def patch(self, path_: str, data_: dict[str, str])->int:
        path = self._patheses.get(
          self._pathFix(path_)
        )
        if 'id' not in data:
            return 1
        _id = data_['id']
        if path not in self._db:
            return 2
        if _id not in self._db[path]:
            return 3
        self._set(path, data_['id'], data_)
        return 0

    """
    get result element copy

    :param:  str : element path
    :param:  list[str] : element list
    :return: list[dict[str,any]] : result element copy
    """
    def _getCopy(self, path_:str, ids_:list[str])->list[dict[str,any]]:
        out = []
        for i in ids_:
            if i in self._db[path_]:
                pack = deepcopy(self._db[path_][i]['data'])
                pack['id'] = deepcopy(self._db[path_][i]['id'])
                out.append(deepcopy(pack))
        return out

    """
    get All record

    :param: str : path
    """
    def _getAll(self, path_:str):
        return self._getCopy(
          path_,
          self._db[
            path_
          ]
        )

    """
    get records by id

    :param: str : path
    :param: list[str] : id list
    """
    def _getId(self, path_: str, ids_: list[str]):
        out = []
        for i in ids_:
            if str(i) in self._db[path_]:
                out.append(str(i))
        return self._getCopy(path_, out)

    """
    get elements by filter

    :param: str : path
    :param: dict[str, str] : filters
    """
    def _getFilter(self, path_: str, filters_: dict[str,str]):
        out = []
        for a in self._db[path_]:
            for b in filters_:
                if b in self._db[path_][a]['data']:
                   for c in filters_[b]:
                       if c in self._db[path_][a]['data'][b]:
                            out.append(str(a))
        return self._getCopy(path_, out)

    """
    get request manager

    :param: str : the record id in str
    """
    def get(self, path_: str, gets_: dict[str,str]):
        path = self._patheses.get(
          self._pathFix(path_)
        )
        if path not in self._db:
            return {}
        if 'id' in gets_:
            return self._getId(path, gets_['id'])
        if gets_ == {}:
            return self._getAll(path)
        else:
            return self._getFilter(path, gets_)


    """

    :param: str|int :  column name 
    :return: dict[str,dict[str, int|list[str]]] : 
    """
    def _columnLen(self, column_:str|int)->int:
        if type(column_) is int:
           return column_
        if type(column_) is float:
           return column_
        return len(column_)

    """

    :param: str :  path name 
    :return: dict[str,dict[str, int|list[str]]] : 
    """
    def columns(self, path_:str)->dict[str,dict[str, int|list[str]]]:
        path = self._patheses.get(
          self._pathFix(path_)
        )
        out = {}
        if path not in self._db:
            return out
        for i in self._db[path]:
             for p in self._db[path][i]['data']:
                 if p not in out:
                     out[p] = {
                         "type" : [str(type(self._db[path][i]['data'][p]).__name__)],
                         "min"  : self._columnLen(self._db[path][i]['data'][p]),
                         "max"  : self._columnLen(self._db[path][i]['data'][p]),
                         "str_min" : len(str(self._db[path][i]['data'][p])),
                         "str_max" : len(str(self._db[path][i]['data'][p]))
                     }
                 else:
                     _type    = str(type(self._db[path][i]['data'][p]).__name__)
                     _len     = self._columnLen(self._db[path][i]['data'][p])
                     _str_len =  len(str(self._db[path][i]['data'][p]))
                     if _type not in out[p]['type']:
                         out[p]['type'].append(_type)
                     if  out[p]['min'] > _len:
                         out[p]['min'] = _len
                     if  out[p]['max'] < _len:
                         out[p]['max'] = _len
                     if  out[p]['str_min'] > _str_len:
                         out[p]['str_min'] = _str_len
                     if  out[p]['str_max'] < _str_len:
                         out[p]['str_max'] = _str_len
        return out

    """

    :param: str :  path name
    :param: str :  column name
    :return: dict[str, any] :
    """
    def columnShow(self, path_:str, column_:str)->dict[str,any]:
        path = self._patheses.get(
          self._pathFix(path_)
        )
        out = {}
        if path not in self._db:
            return out
        for i in self._db[path]:
             if column_ in self._db[path][i]['data']:
                 out[str(i)] = self._db[path][i]['data'][column_]
        return out

    """

    :param: str :  path name 
    :return: int : count records in path
    """
    def count(self, path_:str)->int:
        out = 0
        path = self._patheses.get(
          self._pathFix(path_)
        )
        if path in self._db:
            for i in self._db[path]:
                out = out + 1
        return out


    """
    :return: int : count all records
    """
    def countAll(self)->int:
        out = 0
        for a in self._db:
            for i in self._db[a]:
                out = out + 1
        return out

