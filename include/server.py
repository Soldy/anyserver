
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from copy import deepcopy 
import os
import json
import logging
import database

_logging      = logging
_initted_     = False
_host_        = 'localhost'
_port_        = 8008
_log_level_   = logging.INFO

def init(logging_, config_ dict[str, str|bool|int]):
    global _initted_
    global _host_
    global _port_
    global _logging
    if _innitted_:
        return
    if "host" in config_:
        _host_ = config["host"]
    if "port" in config_:
        _port_ = config["port"]
    _logging = logging_
    database.init(logging_, config_)
    _initted_ = True

class Server(BaseHTTPRequestHandler):
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
        database.get(
            self._clearPath(),
            self._get_variables()
        )
    def do_POST(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        database.post(post_data)
        self._do_response(json.dumps('{}'))
    def do_DELETE(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        database.delete(post_data)
        self._do_response(json.dumps('{}'))
    def do_PATCH(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        database.path(post_data)
        self._do_response(json.dumps('{}'))
    def log_message(self, format, *args: list[str]):
        global _logging
        if len(args) == 3:
            _logging.info(args[0]+" "+args[1]+" "+args[2])
            return
        out = ''
        for i in args:
            out = out + str(i)
        _logging.info(out)
        return

def _httpServer(server_class=HTTPServer, handler_class=Server, port=8008, host='127.0.0.1', protocol_version='HTTP/1.1'):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class, protocol_version)
    _logging.info('httpd starting')
    httpd.serve_forever()

def start():
    global _host_
    global _port_
    _httpServer(host=_host_, port=_port_)
