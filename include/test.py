
"""
" pytest
"""
import pytest
import time
import requests
from conf import test as configStart
from log import start as logStart
from server import start as serverStart
from threading import Thread
import multiprocessing

_config = configStart({
  "load" : False,
  "save" : False
})
_proc = multiprocessing.Process(
   target=serverStart, args=[
     logStart(_config),
     _config
])
_response = ''

def test_serverStart():
    """ get request  """
    global _proc
    _proc.start()
    time.sleep(1)
    assert (_proc.is_alive())

@pytest.mark.skipif(not test_serverStart, reason='anyserver start failed no reson to test')
def test_simpleGet():
    """ get request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/'
    )
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.skipif(not test_serverStart, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGet():
    """ get test request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/test'
    )
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )
@pytest.mark.skip(reason='incorrect implementation')
def test_simpleTestRouteGetById():
    """ get test by id request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/test?id=1'
    )
    assert (_response.status_code == 404)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.skipif(not test_serverStart, reason='anyserver start failed no reson to test')
def test_simpleTestRoutePost():
    """ post test route request  """
    global _response
    data = {'test': 'lorem ipsum'}
    _response = requests.post(
      'http://localhost:8008/test/',
      json = data
    )
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.skipif(not test_serverStart, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetAfterPost():
    """ get test route request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/test/',
    )
    assert (_response.status_code == 200)
    assert (_response.text == '[{"test": "lorem ipsum", "id": "1"}]')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.skipif(not test_serverStart, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetByIdAfterPost():
    """ get test by id request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/test/?id=1'
    )
    assert (_response.status_code == 200)
    assert (_response.text == '[{"test": "lorem ipsum", "id": "1"}]')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

def test_serverSop():
    """ start server  """
    global _proc
    _proc.terminate()
    time.sleep(1)
    assert _proc.is_alive() is False
