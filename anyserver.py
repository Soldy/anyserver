from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from copy import deepcopy 
import os
import json
import time
import logging
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", dest="port",
  help="listen port", metavar="PORT", default="8008")
parser.add_argument("-l", "--host", dest="host",
  help="listen host", metavar="HOST", default="localhost")
parser.add_argument("-d", "--db", dest="db",
  help="data collection directory", metavar="DB", default="db")
parser.add_argument("--index", dest="index",
  help="index collection", metavar="INDEXFILE", default="indexes.json")
parser.add_argument("--path", dest="path",
  help="url path collection file", metavar="PATHFILE", default="pathes.json")
parser.add_argument("--save", dest="save",
  help="save the datacollection", metavar="True/False", default=True)
parser.add_argument("--load", dest="load",
  help="load the datacollection at the start", metavar="True/False", default=True)
args = parser.parse_args()

_config = {
    "port"   : 8008,
    "host"   : "localhost",
    "db_dir" : "db",
    "index"  : "indexes.json",
    "path"   : "pathes.json",
    "log"    : logging.DEBUG,
    "load"   : True,
    "save"   : True
}


"""
Multipath manager class.
"""
class PathesClass:
    def __init__(self, logging_, config_):
        self._log    = logging_
        self._config = config_
        self._serial = 0
        self._path   = {}
        self.check()

    """
    Path cache check
    """
    def check(self)->bool:
        _error = False
        if not self._config['load']:
            return False
        if not self._config['save']:
            return False
        if not os.path.exists(
          self._config['path'],
        ):
            self._log.info('Creating index file')
            with open(
              self._config['path'],
              'w'
            ) as file_:
                json.dump({}, file_)
        if not os.path.isfile(
          self._config['path'],
        ):
            self._log.critical('Path file error')
            return True
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
               self._serial = int(self._path[i]) + 1
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
Index class.
"""
class IndexesClass:
    def __init__(self, logging_, config_):
        self._log = logging_
        self._config = config_
        self._ids = {}
        self._index = {}

    """
    Index cache check
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
    def add(self, path_:str, id_:str):
        if path_ not in self._index:
            self._index[path_] = []
        if id_ not in self._index:
            self._index[path_].append(deepcopy(id_))
            self.save()
    def addId(self, path_:str)->str:
        if path_ not in self._ids:
            self._ids[path_] = 0
        self._ids[path_] = self._ids[path_] + 1
        return deepcopy(str(self._ids[path_]))
    def all(self, path_:str):
        if path_ not in self._index:
            return []
        return deepcopy(self._index[path_])


class DatabasesClass:
    def __init__(self, logging_, config_):
        self._log = logging_
        self._config = config_
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
        self._patheses.load()
        self._indexes.load()
        self.loadAll()
    """
    path name fix
    """
    def _pathFix(self, path_:str)->str:
        return path_.replace("/", "_")
    """ This checking the file system for initialization. """
    def check(self):
        _error = False
        if not self._config["save"]:
            return
        if not self._config["load"]:
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
        self._indexes.add(path_, id_)
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
        _id = self._indexes.addId(
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



class Server(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self._logging = logging
        BaseHTTPRequestHandler.__init__(self, *args)
    def _clearPath(self)->str:
        if '?' not in self.path:
           return deepcopy(self.path)
        return deepcopy(self.path[:self.path.index('?')])
    def _getVariables(self)->dict[str,str]:
        out = {}
        if '?' not in self.path:
           return out
        start = self.path.index('?')+1
        var_string = self.path[start:]
        if '&' in var_string:
           var_array = var_string.split('&')
        else:
           var_array = [var_string]
        for block in var_array:
            if '=' in block:
                pos = block.index('=')
                value = block[pos+1:]
                key = block[:pos]
                if key not in out:
                   out[key] = []
                out[key].append(value)
        return out
    def _do_response(self, data_: str):
        out = data_.encode()
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header('Protocol-Version', "HTTP/1.1")
        self.send_header('Content-type', 'application/json')
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
        self._do_json_response(
          _db.get(
            self._clearPath(),
            self._getVariables()
          )
        )
    def do_POST(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        _db.post(
          self._clearPath(),
          post_data
        )
        self._do_response(json.dumps('{}'))
    def do_PATCH(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        database.path(post_data)
        self._do_response(json.dumps('{}'))
    def log_message(self, format, *args: list[str]):
        if len(args) == 3:
            self._logging.info(args[0]+" "+args[1]+" "+args[2])
            return
        out = ''
        for i in args:
            out = out + str(i)
        self._logging.info(out)
        return

def _httpServer(server_class=HTTPServer, handler_class=Server, port=8008, host='127.0.0.1', protocol_version='HTTP/1.1'):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class, protocol_version)
    logging.debug("httpd starting "+host+":"+str(port))
    httpd.serve_forever()

def start(args):
    global _config
    if str(int(args.port)) != args.port:
       logging.critical("invalid port")
       quit()
    _config["port"] = int(args.port)
    _config["host"] = args.host
    _config["db_dir"] = args.db
    _config["index"] = args.index
    _config["path"] = args.path
    if args.load == False:
        _confif["load"] = False
    if args.save == False:
        _confif["save"] = False
    _httpServer(host=_config["host"], port=_config["port"])

"""
server init
"""
logging.basicConfig(
  format='%(asctime)s - %(levelname)s - %(message)s',
  level=_config['log']
)

_db = DatabasesClass(logging, _config)

if __name__ == "__main__":
    start(args)
