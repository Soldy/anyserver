from copy import deepcopy 
from sys import argv
import os
import json
import time
import include.path
import include.index

_db_   = {}

_save_ = True
_load_ = True



"""
Db record file name 

:param: str : the record id in str
:return: str: full path 
"""
def fileName(path_: str, id_: str)->str:
    return (
        _db_dir_+
        '/'+
        path_+
        '/'+
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


