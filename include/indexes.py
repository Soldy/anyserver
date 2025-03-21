from copy import deepcopy 
from sys import argv
import os
import json
import logging

_file_  = 'indexes.json'
_ids_ = {}
_index_ = {}
_log_level_   = logging.INFO


def check()->bool:
    _error = False
    if not os.path.exists(_file_):
        logging.info('Creating index file')
        with open(_file_, 'w') as file_:
            json.dump({}, file_)
    if not os.path.isfile(_file_):
        logging.critical('Index file error')
        return True
    return False

def save():
    global _index_
    with open(_file_, 'w') as file_:
        json.dump(_index_, file_)

def read():
    global _index_
    with open(_file_, 'r') as file_:
         _index_ = json.load(file_)

def add(path_:str, id_:str)->int:
    global _index_
    if path_ not in _index_:
        _index_[path_] = []
    if id_ not in _index_:
        _index_[path_].append(deepcopy(id_))
        _indexSave()

def addId(path:str)->str:
    global _ids_
    if path_ not in _ids_:
        _ids_[path_] = 0
    _ids_[path_] = _ids_[path_] + 1
    return deepcopy(str(_id_[path_]))
