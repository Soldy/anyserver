
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from copy import deepcopy 
import os
import json
import forward
import database
from database import DatabasesClass
from databasedbm import DatabasesDbmClass

_db = ''
_forward = ''
_logging = ''



class Server(BaseHTTPRequestHandler):
    def __init__(self, *args):
        global _logging
        global _db
        global _forward
        self._logging = _logging
        self._db= _db
        self._forwarder = _forward
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
        result = self._forwarder.forward(
          self.path,
          self.headers,
          'GET',
          '{}'
        )
        if result == '{}':
          return self._do_json_response(
            self._db.get(
              self._clearPath(),
              self._getVariables()
            )
          )
        return self._do_json_response(result)

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
    global _forward
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
    _forward = forward.ForwarderClass(_db, logging_, config_)
    _logging = logging_
    _httpServer(logging_, host=config_["host"], port=config_["port"])



