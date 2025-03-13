from http.server import BaseHTTPRequestHandler, HTTPServer
from copy import deepcopy 
import json
import time
import datetime

_id_ = 0
_data_base_ = {}

def dateTimeNow()->str:
    return (
        datetime.
        datetime.
        now().
        replace(tzinfo=datetime.timezone.utc).
        isoformat()
    )


hostName = "localhost"
serverPort = 8080
def _postSave_(data):
    global _id_
    global _data_base_
    now = dateTimeNow()
    _id_ = _id_ + 1
    data['id'] = _id_
    data['is_active'] = True
    data['created_at'] = deepcopy(now)
    data['updated_at'] = deepcopy(now)
    _data_base_[str(_id_)] = data

def _postEdit_(data_):
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


def _delete_(ids_ : list[int]):
    for i in range(len(ids_)):
         if str(ids_[i]) in _data_base_:
             _data_base_[str(ids_[i])]['is_active'] = False

def _getCopy_(result_):
    out = []
    for i in result_:
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

def _getFilter_(filters_):
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
        print(self.requestline)
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
            pos = block.index('=')
            value = block[pos+1:]
            key = block[:pos]
            if key not in out:
                out[key] = []
            out[key].append(value)
        return out
    def _do_response(self, data):
        out = data.encode()
        self.send_response(200)
        self.protocol_version = 'HTTP/1.1'
        self.send_header('Protocol-Version', "HTTP/1.1")
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-length', len(out))
        self.end_headers()
        self.wfile.write(out)
    def _do_json_response(self, data_):
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
        print(post_data)
        _delete_(post_data)
        self._do_response(json.dumps('{}'))
    def do_PATCH(self):
        length = int(self.headers['content-length'])
        field = self.rfile.read(length).decode()
        post_data = json.loads(field)
        _postEdit_(post_data)
        self._do_response(json.dumps('{}'))


def run(server_class=HTTPServer, handler_class=Server, port=8008,  protocol_version='HTTP/1.1'):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class, protocol_version)
    print ('Starting httpd on port')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 3:
        run(port=int(argv[1]))
    else:
        run()
