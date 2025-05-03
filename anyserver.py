import os
import math
import time
import json
import dbm.gnu
import logging
import argparse
import datetime
from urllib import parse
from copy import deepcopy
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler

parser = argparse.ArgumentParser()
parser.add_argument("--port",
  type=int,
  dest="port",
  help="listen port",
  metavar="PORT",
  default="8008")
parser.add_argument("-l", "--host",
  type=str,
  dest="host",
  help="listen host",
  metavar="HOST",
  default="localhost"
)
parser.add_argument(
  "--store_type",
  dest="store_type",
  choices=["json", "dbm"],
  default="json"
)
parser.add_argument("--db_dir",
  type=str,
  dest="db_dir",
  help="data collection directory",
  metavar="DB",
  default="db"
)
parser.add_argument("--dbm_dir",
  type=str,
  dest="dbm_dir",
  help="dbm data collection directory",
  metavar="DBM",
  default="dbm"
)
parser.add_argument("--index_file",
  type=str,
  dest="index_file",
  help="index collection",
  metavar="INDEXFILE",
  default="indexes.json"
)
parser.add_argument("--index_dbm",
  type=str,
  dest="dbm_index",
  help="index collection in dbm",
  metavar="INDEXDBM",
  default="indexes.dbm"
)
parser.add_argument("--path_file",
  type=str,
  dest="path_file",
  help="url path collection file",
  metavar="PATHFILE",
  default="pathes.json"
)
parser.add_argument("--path_dbmn",
  type=str,
  dest="dbm_path",
  help="url path collection dbm",
  metavar="PATHDBM",
  default="pathes.dbm"
)
parser.add_argument("--save",
  dest="save",
  help="save the datacollection",
  action='store_false'
)
parser.add_argument("--load",
  dest="load",
  help="load the datacollection at the start",
  action='store_false'
)
parser.add_argument("--log_level",
  type=int,
  dest="log_level",
  help="log level 10 - 50",
  metavar="LOG_LEVEL",
  default="50"
)
parser.add_argument("--vv",
  dest="vv",
  help="Verbose log equal with --log_level 10",
  action='store_true'
)



_config = {
    'port'       : 8008,
    'host'       : 'localhost',
    'forward'    : '',
    'db_dir'     : 'db',
    'store_type' : 'json',
    'index'      : 'indexes.json',
    'path'       : 'pathes.json',
    'dbm_path'   : 'pathes.dbm',
    'dbm_index'  : 'indexes.dbm',
    'dbm_dir'    : 'dbm',
    'log_level'  : 10,
    'load'       : True,
    'save'       : True,
    'dummy_test' : 'dummy'
}


"""
config processor

:return: dict[str,str]
"""
def confInit (args, logging_)->dict[str,str]:
    global _config
    if int(str(int(args.port))) != args.port:
       logging_.critical('invalid port')
       quit()
    if args.port > 65535:
       logging_.critical('invalid port to big number')
       quit()
    if args.port < 1:
       logging_.critical('invalid port to low number')
       quit()
    if int(str(int(args.log_level))) != args.log_level:
       logging_.critical('invalid log level')
       quit()
    if args.log_level > 50:
       logging_.critical('invalid log level to big number')
       quit()
    if args.log_level < 10:
       logging_.critical('invalid log level low number')
       quit()

    _config['port'] = int(args.port)
    _config['log_level'] = int(args.log_level)
    _config['store_type'] = args.store_type
    _config['host'] = args.host
    _config['db_dir'] = args.db_dir
    _config['dbm_dir'] = args.dbm_dir
    _config['index'] = args.index_file
    _config['dbm_index'] = args.dbm_index
    _config['path'] = args.path_file
    _config['dbm_path'] = args.dbm_path
    if args.load == False:
        _config['load'] = False
    if args.save == False:
        _config['save'] = False
    if args.vv:
        _config['log_level'] = 10
    return _config

"""
log init

:param: dict[str,str]
"""
def logStart (config_: dict[str,str])->logging:
    logging.basicConfig(
      format='%(asctime)s - %(levelname)s - %(message)s',
      level=config_['log_level']
    )
    return logging

"""
Index class.
"""
class IndexesClass:
    def __init__(self, logging_, config_):
        self._log = logging_
        self._config = config_
        self._ids = {}
        self._index = {}

    """
    Index cache load 
    """
    def load(self):
        if not self._config['load']:
            return
        self._log.debug(
          'Loading indexes file'
        )
        with open(self._config['index'], 'r') as file_:
            self._index = json.load(file_)
        for path in self._index:
            if path not in self._ids:
                self._ids[path] = 0
            for i in self._index[path]:
                if int(i) > self._ids[path]:
                    self._ids[path] = int(i)

    """
    Index cache check

    :return: bool
    """
    def check(self)->bool:
        _file_ = self._config['index']
        _error = False
        if not self._config['load']:
            return False
        if not self._config['save']:
            return False
        if not os.path.exists(_file_):
            self._log.info('Creating index file')
            with open(_file_, 'w') as file_:
                json.dump({}, file_)
        if not os.path.isfile(_file_):
            self._log.critical('Index file error')
            return True
        self.load()
        return False

    """
    Index cache save
    """
    def save(self):
        if not self._config['save']:
            return
        _file_ = self._config['index']
        with open(self._config['index'], 'w') as file_:
            json.dump(self._index, file_)

    """
    add new index 

    :param: str
    :param: str
    """
    def _addIndex(self, path_:str, id_:str):
        if path_ not in self._index:
            self._index[path_] = []
        if id_ not in self._index[path_]:
            self._index[path_].append(deepcopy(id_))
            self.save()

    """
    add new id

    :param: str
    """
    def _addId(self, path_:str):
        if path_ not in self._ids:
            self._ids[path_] = 0
        self._ids[path_] = self._ids[path_] + 1

    """
    add public function

    :param: str
    :return: str
    """
    def add(self, path_:str)->str:
        self._addId(path_)
        self._addIndex(path_, str(self._ids[path_]))
        return str(self._ids[path_])


    """
    all index in path

    :param: str
    :return: list[str]
    """
    def all(self, path_:str)->list[str]:
        if path_ not in self._index:
            return []
        return deepcopy(self._index[path_])


"""
Index class.
"""
class IndexesDbmClass:
    def __init__(self, logging_, config_):
        self._log    = logging_
        self._config = config_
        self._ids    = {}
        self._index  = {}
        self._db     = dbm.gnu.open(
          self._config['dbm_index'],
          'cs'
        )

    """
    Index dbm check
    :return: bool : False
    """
    def check(self)->bool:
        return False

    """
    temp dummy save
    """
    def save(self):
        return

    """
    temp dummy load 
    """
    def load(self):
        return

    """
    get an index id in the path

    :param: str : path_
    :return: dict[str,int|list[str]]
    """
    def get(self, path_:str)->dict[str,int|list[str]]:
        return json.loads(
          self._db.get(
            path_,
            b'{"serial":0,"index":[]}'
          ).decode("utf-8")
        )

    """
    add an index id to the path

    :param: str : path_
    :return: str
    """
    def add(self, path_:str)->str:
        current = self.get(path_)
        current['serial'] = current['serial'] + 1
        current['index'].append(
          str(current['serial'])
        )
        self._db[path_] = json.dumps(current)
        return str(current['serial'])

    """
    get all indexes

    :param: str : path_
    :return: str
    """
    def all(self, path_:str):
        return deepcopy(self.get(path_)['index'])


"""
Multipath manager class.
"""
class PathesClass:
    def __init__(self, logging_, config_):
        self._log    = logging_
        self._config = config_
        self._serial = 0
        self._path   = {}

    """
    Path cache load 
    """
    def load(self):
        if not self._config['load']:
            return
        self._log.debug(
          'Loading patheses file'
        )
        with open(
          self._config['path'],
          'r'
        ) as file_:
            self._path = json.load(file_)
        for i in self._path:
            if int(self._path[i]) >= self._serial:
               self._serial = int(self._path[i])

    """
    Path cache check
    """
    def check(self)->bool:
        _file_ = self._config['path']
        _error = False
        if not self._config['load']:
            return False
        if not self._config['save']:
            return False
        if not os.path.exists(_file_):
            self._log.info('Creating index file')
            with open(
              _file_,
              'w'
            ) as file_:
                json.dump({}, file_)
        if not os.path.isfile(_file_):
            self._log.critical('Path file error')
            return True
        self.load()
        return False

    """
    Path cache save
    """
    def save(self):
        if not self._config['save']:
            return
        with open(
          self._config['path'],
          'w'
        ) as file_:
           json.dump(self._path, file_)

    def add(self, path_:str)->str:
        if path_ not in self._path:
            self._serial = self._serial + 1
            self. _path[path_] = deepcopy(self._serial)
            self.save()
        return deepcopy(str(self._path[path_]))
    def get(self, path_:str)->str:
        return self.add(path_)
    def all(self):
        return deepcopy(self._path)

"""
Multipath manager class.
"""
class PathesDbmClass:
    def __init__(self, logging_, config_):
        self._log    = logging_
        self._config = config_
        self._serial = 0
        self._db     = dbm.gnu.open(
          self._config['dbm_path'],
          'cs'
        )
    """
    Path dbm check
    :return: bool : False
    """
    def check(self)->bool:
        return False

    """
    temp dummy save
    """
    def save(self):
        return

    """
    temp dummy load 
    """
    def load(self):
        return 

    """
    get a path id

    :param: str : path_
    :return: str
    """
    def get(self, path_:str)->str:
        return str(int(
          self._db.get(path_, b'-1').decode("utf-8")
        ))

    """
    add / generate a path id

    :param: str : path_
    :return: str
    """
    def add(self, path_:str)->str:
        if self.get(path_) == '-1':
            self._serial = self._serial + 1
            self._db[path_] = str(self._serial)
        return self.get(path_)

    """
    get all path

    :param: str : path_
    :return: str
    """
    def all(self):
        out = {}
        key = self._db.firstkey()
        while key is not None:
          out[key.decode('utf-8')] = self._db[key].decode('utf-8')
          key = self._db.nextkey(key)
        return out

class DatabaseHelpClass:
    def __init__(self, logging_):
        self._log     = logging_
        self._checked = False

    """
    path name fix

    :param: str : the record id in str
    :return: str: full path 
    """
    def pathFix(self, path_:str)->str:
        return path_.replace("/", "_")

    """
    check dir existance
    :param: str:
    :return: bool:
    """
    def checkDir(self, dir_:str)->bool:
        if self._checked:
           return False
        if not os.path.exists(
          dir_
        ):
            self._log.debug(
              'Creating database directory'
            )
            os.makedirs(
              dir_
            )
        if not os.path.isdir(
          dir_
        ):
            self._log.critical(
              'Database directory error'
            )
            return True
        self._checked = True
        return False

    """
    create data structure
    """
    def create(
      self,
      id_: int,
      data_: dict[str,any]
    )->dict[str,any]:
        time = math.floor(
          datetime.datetime.timestamp(
            datetime.datetime.now()
          )
        )
        out = {}
        out['data']       = deepcopy(data_)
        out['id']         = deepcopy(id_)
        out['created_at'] = deepcopy(time)
        out['changed_at'] = deepcopy(time)
        return out

    """
    change data structure
    """
    def change(
      self,
      data_: dict[str,any],
      record_: dict[str,any]
    )->dict[str,any]:
        record = {}
        record['id'] = data_['id']
        record['created_at'] = data_['created_at']
        time = math.floor(
          datetime.datetime.timestamp(
            datetime.datetime.now()
          )
        )
        record['data']       = {**data_['data'], **record_}
        record['changed_at'] = time
        return deepcopy(record)
    def extend(
      self,
      data_: dict[str,any],
      record_: dict[str,any]
    )->dict[str,any]:
        out = deepcopy(record_['data'])
        for i in data_:
            out[i] = data_[i]
        return self.change(out, record_)

    """
     output data format
    """
    def outdata(
      self,
      data_: dict[str,any]
    )->dict[str,any]:
        if data_ == {}:
            return {}
        out       = deepcopy(data_['data'])
        out['id'] = deepcopy(data_['id'])
        return out


class DatabasesClass:
    def __init__(self, logging_, config_):
        self._log = logging_
        self._config = config_
        self._helper = DatabaseHelpClass(
          self._log
        )
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

    """
    check dir existance
    """
    def _checkDir(self):
        if (not self._config['save'] and
          not self._config['load']):
            return False
        return self._helper.checkDir(
          self._config["db_dir"]
        )

    """
     This checking the file system
     for initialization.
    """
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

    :param: str : the path name
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
    :param: dict[str, str] : record data
    :return: int : result code 0 ok
    """
    def post(
      self,
      path_: str, data_: dict[str, str])->int:
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
          self._helper.pathFix(path_)
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
    def _getCopy(
      self,
      path_:str,
      ids_:list[str]
    )->list[dict[str,any]]:
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
    :param: dict[str,str]
    :param: dict[str, str] : filters
    """
    def _getFilter(
      self,
      path_: str,
      filters_: dict[str,str]
    ):
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
          self._helper.pathFix(path_)
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
          self._helper.pathFix(path_)
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
          self._helper.pathFix(path_)
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
          self._helper.pathFix(path_)
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


class DatabasesDbmClass:
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

    """
    Dbm path file name

    :param: str : the path name
    :return: str: full path 
    """
    def _fileName(self, path_: str)->str:
        return (
          self._config["dbm_dir"]+
          '/'+
          path_+
          '.dbm'
        )

    """
     Checking the file system
     for initialization.
    """
    def check(self):
        return self._helper.checkDir(
          self._config["dbm_dir"]
        )

    """
    Db record post

    :param: str : the record id in str
    :return: int : result code 0 ok
    """
    def post(self,
      path_: str,
      data_: dict[str, str]
    )->int:
        path = self._helper.pathFix(path_)
        db = dbm.gnu.open(
          self._fileName(
            path
          ),
          'cs'
        )
        _id = self._indexes.add(
          self._patheses.get(
            path
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

    def _get(self, db_, id_):
        return self._helper.outdata(
          json.loads(
            db_.get(
              id_,
              b'{}'
            ).decode("utf-8")
          )
        )

    """
    get All record

    :param: str : path
    """
    def _getAll(self, path_:str):
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
              self._get(db,key)
            )
            key = db.nextkey(key)
        db.close()
        return out
    """
    get All record

    :param: str : path
    """
    def _getId(self, path_:str, ids_:list[str]):
        try:
            out = []
            db = dbm.gnu.open(
              self._fileName(
                path_
              ),
              'r'
            )
            for i in ids_:
                dat = self._get(
                  db,
                  str(i)
                )
                if dat != {}:
                    out.append(dat)
            db.close()
            return out
        except Exception:
            return []

    """
    get filter

    :param: str : path
    """
    def _getFilter(
      self,
      path_: str,
      filters_: dict[str,str]
    ):
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
            a = self._get(db,key)
            for b in filters_:
                if b in a:
                   for c in filters_[b]:
                       if c in a[b]:
                           out.append(a)
            key = db.nextkey(key)
        db.close()
        return out
    """
    get request manager

    :param: str : the record id in str
    """
    def get(
      self,
      path_: str,
      gets_: dict[str,str]
    ):
        path = self._helper.pathFix(path_)
        if 'id' in gets_:
            return self._getId(path, gets_['id'])
        if gets_ == {}:
            return self._getAll(path)
        else:
            return self._getFilter(path, gets_)



_db = ''
_logging = ''



class Server(BaseHTTPRequestHandler):
    def __init__(self, *args):
        global _logging
        global _db
        self._logging = _logging
        self._db= _db
        BaseHTTPRequestHandler.__init__(self, *args)
    def _clearPath(self)->str:
        if '?' not in self.path:
           return deepcopy(self.path)
        return deepcopy(self.path[:self.path.index('?')])
    def _getVariables(self)->dict[str,str]:
        if '?' not in self.path:
           return {}
        start = self.path.index('?')+1
        var_string = self.path[start:]
        return parse.parse_qs(var_string)
    def _do_response(self, data_: str):
        out = data_.encode()
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header('Protocol-Version', "HTTP/1.1")
        self.send_header('Content-type', 'application/json; charset=utf8')
        self.send_header('Content-length', len(out))
        self.end_headers()
        self.wfile.write(out)
    def _do_json_response(self, data_: dict[str, any] | list[dict[str, any]]):
        return self._do_response(
            json.dumps(
                data_
            )
        )
    def do_GET(self):
        return self._do_json_response(
          self._db.get(
            self._clearPath(),
            self._getVariables()
          )
        )

    def do_POST(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        self._db.post(
          self._clearPath(),
          post_data
        )
        self._do_response(json.dumps({}))

    def do_PATCH(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        self._do_response(json.dumps({}))

    def log_message(self, format, *args: list[str]):
        if len(args) == 3:
            self._logging.info(args[0]+" "+args[1]+" "+args[2])
            return
        out = ''
        for i in args:
            out = out + str(i)
        self._logging.info(out)
        return


def _httpServer(logging_, server_class=HTTPServer, handler_class=Server, port=8008, host="127.0.0.1", protocol_version="HTTP/1.1"):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class, protocol_version)
    logging_.debug("httpd starting "+host+":"+str(port))
    httpd.serve_forever()

def serverStart(logging_, config_):
    global _db
    global _logging
    if config_['store_type'] == 'json':
        _db = DatabasesClass(
          logging_,
          config_
        )
    else:
        _db = DatabasesDbmClass(
          logging_,
          config_
        )
    _logging = logging_
    _httpServer(logging_, host=config_["host"], port=config_["port"])


if __name__ == "__main__":
   args = parser.parse_args()
   _config = confInit(
     args,
     logging
   )
   serverStart(
     logStart(
       _config
     ),
     _config
  )
