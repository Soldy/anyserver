
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from copy import deepcopy 
import os
import json
import logging
import database

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




class Server(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self._logging = logging
        BaseHTTPRequestHandler.__init__(self, *args)
    def _clearPath(self)->str:
        if '?' not in self.path:
           return deepcopy(self.path)
        return deepcopy(path[:path.index('?')])
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
    logging.debug('httpd starting')
    httpd.serve_forever()

def start():
    global _config
    _httpServer(host=_config['host'], port=_config['port'])

"""
server init
"""
logging.basicConfig(
  format='%(asctime)s - %(levelname)s - %(message)s',
  level=_config['log']
)

_db = database.DatabasesClass(logging, _config)
start()

