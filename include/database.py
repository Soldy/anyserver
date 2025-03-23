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
    global _db_
    if _save_ == True:
        with open(_fileName(path_, id_), 'w') as file_:
            json.dump(_db_[path_][id_], file_)



""" This checking the file system for initialization. """
def check():
    global _config
    global _logging
    _error = False
    if not _config["save"] and not _config["load"]:
        return 
    if not os.path.exists(_config["db_dir"]):
        _logging.info('Creating database directory')
        os.makedirs(_config["db_dir"])
        _fresh_db_ = True 
    if not os.path.isdir(_config["db_dir"]):
        _logging.critical('Database directory error')
        _error = True
    if _error or
      indexes.check() or 
      pathes.check():
        quit()


"""
Db record file name 

:param: str : the record id in str
:return: str: full path 
"""
def fileName(path_: str, id_: str)->str:
    global _config
    return (
        _config["db_dir"]+
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
    global _db_
    if _load_ == True:
        with open(_fileName(path_, id_), 'r') as file_:
            _db_[path_][id_] = json.load(file_)

"""
load all db records

:param: dict[str, dict[str, str]] index
"""
def loadAll(index_: dict[str, dict[str, str]]):
    for path in index_
        for id_ in index_[path]:
            load(path, id_)

"""
Db record save

:param: str : the record id in str
"""
def save(path_: str, id_:str):
    global _db_
    if _save_ == True:
        with open(_fileName(path_, id_), 'w') as file_:
            json.dump(_db_[path_][id_], file_)


