from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from copy import deepcopy 
from sys import argv
import os
import json
import time
import datetime
import logging

_id_ = 0
_index_file_ = 'index.json'
_server_host_ = 'localhost'
_server_port_ = 8008
_data_base_ = {}
_save_data_ = True
_load_data_ = True
_log_level_ = logging.INFO

_fresh_db_ = False
_index_ = []
_db_dir_ = 'db'

def dateTimeNow()->str:
    return (
        datetime.
        datetime.
        now().
        replace(tzinfo=datetime.timezone.utc).
        isoformat()
    )



def _dbExistCheck():
    _error = False
    if not _save_data_ and not _load_data_:
        return 
    if not os.path.exists(_db_dir_):
        logging.info('Creating database directory')
        os.makedirs(_db_dir_)
        _fresh_db_ = True 
    if not os.path.isdir(_db_dir_):
        logging.critical('Database directory error')
        _error = True
    if not os.path.exists(_index_file_):
        logging.info('Creating index file')
        with open(_index_file_, 'w') as file_:
            json.dump([], file_)
        _fresh_db_ = True 
    if not os.path.isfile(_index_file_):
        logging.critical('Index file error')
        _error = True
    if _error:
          quit()

def _fileName(id_:str)->str:
    return (
        _db_dir_+
        '/'+
        str(id_)+
        '.json'
    )

def _dbSave(id_:str):
    global _data_base_
    if _save_data_ == True:
        with open(_fileName(id_), 'w') as file_:
            json.dump(_data_base_[id_], file_)

def _dbRead(id_:str):
    global _data_base_
    with open(_fileName(id_), 'r') as file_:
        _data_base_[id_] = json.load(file_)

def _dbReadAll():
    global _index_
    for i in _index_:
        _dbRead(i)

def _indexSave():
    global _index_
    with open(_index_file_, 'w') as file_:
        json.dump(_index_, file_)

def _indexRead():
    global _index_
    with open(_index_file_, 'r') as file_:
         _index_ = json.load(file_)

def _indexAdd(id_:str)->int:
    global _index_
    if id_ not in _index_:
        _index_.append(id_)
    _indexSave()

def _indexDel(id_:str)->int:
    global _index_
    del _index_[_index_.index(id_)]
    _indexSave()

def _findId():
    global _index_
    global _id_
    for i in  _index_:
        if int(i) > _id_:
            _id_ = deepcopy(int(i))

def _addId()->str:
    global _id_
    _id_ = _id_ + 1
    return deepcopy(str(_id_))


def _postSave_(data_: dict[str, str]):
    global _data_base_
    now = dateTimeNow()
    _id = _addId()
    data_['id'] = _id
    data_['is_active'] = True
    data_['created_at'] = deepcopy(now)
    data_['updated_at'] = deepcopy(now)
    _data_base_[_id] = data_
    _indexAdd(_id)
    _dbSave(_id)

def _postEdit_(data_: dict[str,str]):
    _id = str(data_['id'])
    if 'id' not in data_:
        return
    if _id not in _data_base_:
        return
    if _data_base_[_id]['is_active'] == False:
        return
    data_['is_active'] = True
    data_['created_at'] = _data_base_[_id]['created_at']
    data_['updated_at'] = dateTimeNow()
    _data_base_[_id] = data_
    _dbSave(_id)


def _delete_(ids_ : list[int]):
    for i in range(len(ids_)):
         if str(ids_[i]) in _data_base_:
             _data_base_[str(ids_[i])]['is_active'] = False

def _getCopy_(ids_:list[str]):
    out = []
    for i in ids_:
        if _data_base_[i]['is_active']:
             out.append(deepcopy(_data_base_[i]))
             out[len(out)-1]['is_active'] = 'true'
    return out

def _getAll_():
    global _data_base_
    return _getCopy_(_data_base_)

def _getId_(ids_):
    global _data_base_
    out = {}
    for i in ids_:
        if str(i) in _data_base_:
            out[str(i)] = _data_base_[str(i)]
    return _getCopy_(out)

def _getFilter_(filters_: dict[str,str]):
    global _data_base_
    out = {}
    for a in _data_base_:
        for b in filters_:
            if b in _data_base_[a]:
                for c in filters_[b]:
                    if c in _data_base_[a][b]:
                        out[a] = _data_base_[a]
    return _getCopy_(out)




class Server(BaseHTTPRequestHandler):
    def _get_variables(self):
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
    def _do_response(self, data_: dict[str, any]):
        out = data_.encode()
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header('Protocol-Version', "HTTP/1.1")
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', len(out))
        self.end_headers()
        self.wfile.write(out)
    def _do_json_response(self, data_: dict[str, any]):
        return self._do_response(
            json.dumps(
                data_
            )
        )
    def do_GET(self):
        gets = self._get_variables()
        if 'id' in gets:
            return self._do_json_response(
                _getId_(gets['id'])
            )
        if gets == {}:
            return self._do_json_response(
                _getAll_()
            )
        else:
            return self._do_json_response(
                _getFilter_(gets)
            )
    def do_POST(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        _postSave_(post_data)
        self._do_response(json.dumps('{}'))
    def do_DELETE(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        _delete_(post_data)
        self._do_response(json.dumps('{}'))
    def do_PATCH(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        _postEdit_(post_data)
        self._do_response(json.dumps('{}'))
    def log_message(self, format, *args: list[str]):
        if len(args) == 3:
            logging.info(args[0]+" "+args[1]+" "+args[2])
            return
        out = ''
        for i in args:
            out = out + str(i)
        logging.info(out)
        return


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=_log_level_)

_dbExistCheck()

if _load_data_ and not _fresh_db_:
    _indexRead()
    _dbReadAll()
    _findId()



def run(server_class=HTTPServer, handler_class=Server, port=8008, host='127.0.0.1', protocol_version='HTTP/1.1'):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class, protocol_version)
    logging.info('httpd starting')
    httpd.serve_forever()
   

if __name__ == "__main__":
        run(host=_server_host_, port=_server_port_)
