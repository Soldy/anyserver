import http.client
from copy import deepcopy 


class ForwarderClass():
    def __init__(self, db_):
        self._host = globForHost
        self._db = db_
    def _headerProcess(self, headers):
        out = {}
        remove = ['host', 'content-length']
        for h in headers:
            if h.lower() not in remove: 
                out[h] = headers[h]
        out['HOST'] = self._host
        return out
    def forward(self, path, headers, method, body):
       if method == 'POST':
           self.post(
             path,
             self._headerProcess(headers)
             body
           )

    def get(self, path, headers):
       self._headerProcess(headers)
    def post(self, path, headers,body):
       conn = http.client.HTTPSConnection(host)
       conn.request("POST", path, body ,headers)
       response = conn.getresponse()
       self._headerProcess(headers)
    def path(self):
       self._headerProcess(headers)
