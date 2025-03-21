from copy import deepcopy 
from sys import argv
import os
import json
import logging

_file_  = 'pathes.json'
_serial_ = 0
_path_ = {}
_log_level_   = logging.INFO

def check()->bool:
    _error = False
    if not os.path.exists(_file_):
        logging.info('Creating index file')
        with open(_file_, 'w') as file_:
            json.dump({}, file_)
    if not os.path.isfile(_file_):
        logging.critical('Path file error')
        return True
    return False

def save():
    global _path_
    with open(_file_, 'w') as file_:
        json.dump(_path_, file_)

def read():
    global _path_
    with open(_file_, 'r') as file_:
        _path_ = json.load(file_)

def add(path_:str)->int:
    global _path_
    global _serial_
    if path_ not in _path_:
        _serial_ = deepcopy(_serial_ + 1)
        _path_[path_] = _serial_
        save()
    return _path_[path_]

def get(path_:str)->int:
    return add(path_)
