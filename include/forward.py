import http.client
from copy import deepcopy 


class ForwarderClass():
    def __init__(self, db_, logging_, config_):
        self._db = db_
        self._config = config_
    def _headerProcess(self, headers):
        out = {}
        remove = ['host', 'content-length']
        for h in headers:
            if h.lower() not in remove: 
                out[h] = headers[h]
        out['HOST'] = self._config['forward']
        return out
    def forward(self, path, headers, method, body):
       if self._config['forward'] == '':
          return '{}'
       if method == 'GET':
           return self.post(
             path,
             self._headerProcess(headers)
           )
       if method == 'POST':
           return self.post(
             path,
             self._headerProcess(headers),
             body
           )

    def get(self, path, headers):
       self._headerProcess(headers)
       return '{}'
    def post(self, path, headers,body):
       conn = http.client.HTTPSConnection(host)
       conn.request("POST", path, body ,headers)
       response = conn.getresponse()
       self._headerProcess(headers)
       return '{}'
    def path(self):
       self._headerProcess(headers)
       return '{}'
