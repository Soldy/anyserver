"""
server management
"""
import json
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from restfullmonkey.log import logInit
from restfullmonkey.database import DatabasesClass

class Server(BaseHTTPRequestHandler):
    """
    basehttprequest implementation
    """
    def __init__(self, logging_, db_, *args):
        self._logging = logging_
        self._db= db_
        super().__init__(*args)

    def _clearPath(self)->str:
        """
        Removing the copy method from here
        will break other functionalities.
        DO NOT REMOVE THIS COPY str() FUNCTION! 

        :return: str
        """
        if '?' not in self.path:
            return str(self.path)
        return str(self.path[:self.path.index('?')])
    def _getVariables(self)->dict[str,str]:
        """
         This function returns the possible variable.
         Post has the priority after the get values.
         DO NOT REMOVE THE POST VALUE READING.
         This tool is built to help with software development.
         Testing and manipulation are easier if 
         the POST variable can be replaced with GET variables.

        :return: dict[str,str]
        """

        if hasattr(self, 'query_data'):
            return parse.parse_qs(self.query_data)
        if '?' not in self.path:
            return {}
        start = self.path.index('?')+1
        var_string = self.path[start:]
        return parse.parse_qs(var_string)
    def _do_response(
      self,
      data_: str,
      status_code : int = 200
    )->None:
        """
        The response value cannot be empty.
        The empty response is always [] or {}.
        The response is hardcoded as JSON, so it cannot be bytes.
        This is a RESTful dev server tool, not a picture storage.
        HTTP version has to be defined, or frameworks are not going to work.

        :param: str
        :param: int
        :return: None
        """
        out = data_.encode()
        self.protocol_version = 'HTTP/1.1'
        self.send_response(status_code)
        self.send_header('Protocol-Version', "HTTP/1.1")
        self.send_header('Content-type', 'application/json; charset=utf8')
        self.send_header('Content-length', len(out))
        self.end_headers()
        self.wfile.write(out)
    def _do_json_response(
      self,
      data_: dict[str, any] | list[dict[str, any]],
      status_code : int = 200
    )->None:
        """
        :param: dict[str, any] | list[dict[str, any]]
        :param: int
        :return: None
        """
        self._do_response(
            json.dumps(
                data_
            ),
            status_code
        )
    def do_GET(self):
        """
        GET request handler.
        """
        try:
            self._do_json_response(
              self._db.get(
                self._clearPath(),
                self._getVariables()
              )
            )
        except Exception:
            self._logging.exception("GET failed for %s", self.path)
            self._logging.exception(traceback.format_exc())
            self._do_json_response({},500)

    def do_POST(self):
        """
        POST request handler.
        """
        try:
            length = int(self.headers['content-length'])
            field = self.rfile.read(length).decode()
            post_data = json.loads(field)
            out = self._db.post(
              self._clearPath(),
              post_data
            )
            self._do_json_response(out)
        except Exception:
            self._logging.exception("POST failed for %s", self.path)
            self._logging.exception(traceback.format_exc())
            self._do_json_response({},500)

    def do_PATCH(self):
        """
        PATCH request handler.
        """
        self._do_json_response({},501)

    def do_DELETE(self):
        """
        DELETE request handler.
        """
        self._do_json_response({},501)

# pylint: disable=W0622
    def log_message(self, format, *args: list[str]):
        """
        Custom logging behavior.
        """
        if len(args) == 3:
            self._logging.info(args[0]+" "+args[1]+" "+args[2])
            return
        self._logging.info(' '.join(str(arg) for arg in args))
# pylint: enable=W0622



def serverStart(config_):
    """
    server start
    """
    logging_ = logInit(
      config_
    )
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
