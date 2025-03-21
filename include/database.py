from copy import deepcopy 
from sys import argv
import os
import json
import time
import pathes
import indexes
import logging

_config = {
    "db_dir" : "db",
    "load"   : True,
    "save"   : True
}
_logging      = logging
_initted_     = False
_db_          = {}

def init(logging_, config_ dict[str, str]):
    global _initted_
    global _config
    if _initted_:
        return
    for i in _config:
        if i in config_:
            _config[i] = config_[i]
    _initted_ = True


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


