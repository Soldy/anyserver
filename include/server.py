
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from copy import deepcopy 
import os
import json
import database

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

def _httpServer(logging_, server_class=HTTPServer, handler_class=Server, port=8008, host="127.0.0.1", protocol_version="HTTP/1.1"):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class, protocol_version)
    logging_.debug("httpd starting "+host+":"+str(port))
    httpd.serve_forever()

def start(logging_, config_):
    global _db
    global _logging
    _db = database.DatabasesClass(
      logging_,
      config_
    )
    _logging = logging_
    _httpServer(logging_, host=config_["host"], port=config_["port"])



