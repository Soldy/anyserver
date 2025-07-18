"""
server management
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from copy import deepcopy
from restfullmonkey.database import DatabasesClass

class Server(BaseHTTPRequestHandler):
    """
    basehttprequest implementation
    """
    def __init__(self, logging_, db_, *args):
        self._logging = logging_
        self._db= db_
        BaseHTTPRequestHandler.__init__(self, *args)
    def _clearPath(self)->str:
        """
        :return: str
        """
        if '?' not in self.path:
            return deepcopy(self.path)
        return deepcopy(self.path[:self.path.index('?')])
    def _getVariables(self)->dict[str,str]:
        """
        :return: dict[str,str]
        """

        if hasattr(self, 'query_data'):
            return parse.parse_qs(self.query_data)
        if '?' not in self.path:
            return {}
        start = self.path.index('?')+1
        var_string = self.path[start:]
        return parse.parse_qs(var_string)
    def _do_response(self, data_: str):
        """
        :param: str
        """
        out = data_.encode()
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header('Protocol-Version', "HTTP/1.1")
        self.send_header('Content-type', 'application/json; charset=utf8')
        self.send_header('Content-length', len(out))
        self.end_headers()
        self.wfile.write(out)
    def _do_json_response(self, data_: dict[str, any] | list[dict[str, any]]):
        """
        :param: dict[str, any] | list[dict[str, any]]:
        """
        return self._do_response(
            json.dumps(
                data_
            )
        )
    def do_GET(self):
        """
        get
        """
        return self._do_json_response(
          self._db.get(
            self._clearPath(),
            self._getVariables()
          )
        )

    def do_POST(self):
        """
        post
        """
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        self._db.post(
          self._clearPath(),
          post_data
        )
        self._do_response(json.dumps({}))

    def do_PATCH(self):
        """
        patch 
        """
#       length = int(self.headers['content-length'])
#       field = self.rfile.read(length).decode()
#       post_data = json.loads(field)
#       self._do_response(json.dumps({}))

# pylint: disable=W0622
    def log_message(self, format, *args: list[str]):
        """
        log
        """
        if len(args) == 3:
            self._logging.info(args[0]+" "+args[1]+" "+args[2])
            return
        out = ''
        for i in args:
            out = out + str(i)
        self._logging.info(out)
        return
# pylint: enable=W0622



def serverStart(logging_, config_):
    """
    server start
    """
    db = DatabasesClass(
      logging_,
      config_
    )
    def ServerLayer(*args):
        return Server(logging_, db, *args)
    host=config_["host"]
    port=config_["port"]
    server_address = (host, port)
    httpd = HTTPServer(server_address, ServerLayer)
    logging_.debug("httpd starting "+host+":"+str(port))
    httpd.serve_forever()
