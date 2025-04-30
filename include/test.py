
"""
" pytest
"""
import pytest
import time
import requests
from conf import test as configStart
from log import start as logStart
from server import start as serverStart
import server
from threading import Thread
import multiprocessing

_config = configStart({
  'load' : False,
  'save' : False
})
_proc = multiprocessing.Process(
   target=serverStart, args=[
     logStart(_config),
     _config
])
_auth_key = ''
_response = ''



def authGet(headers_):
    auth = {
      'Authorization' : 'Bearer '+_auth_key
    }
    return {**headers_, **auth}

def requestGet(route_, headers_):
    return requests.get(
      'http://localhost:8008' + route_,
      headers = authGet(headers_)
    )

def test_config():
    config = configStart({
      'load' : False,
      'save' : True
    })
    assert (config['load'] == False)
    assert (config['save'] == True)
    assert (config['dummy_test'] == 'dummy')


def test_configAgain():
    config = configStart({
      'load' : True,
      'save' : False,
      'dummy_test' : 'd2ummy'
    })
    assert (config['load'] == True)
    assert (config['save'] == False)
    assert (config['dummy_test'] == 'd2ummy')

def test_pathNoSave():
    config = configStart({
      'load' : False,
      'save' : False,
    })
    pathes = server.database.pathes.PathesClass(
      logStart(_config),
      config
    )
    assert(pathes.add('_') == '1')
    assert(pathes.add('test') == '2')

def test_pathSave():
    config = configStart({
      'path' : 'pathes_test.json',
      'load' : True,
      'save' : True,
    })
    pathes = server.database.pathes.PathesClass(
      logStart(_config),
      config
    )
    pathes.check()
    pathes.load()
    assert(pathes.add('_') == '1')
    assert(pathes.add('test') == '2')

def test_pathSaveAndLoad():
    config = configStart({
      'path' : 'pathes_test.json',
      'load' : True,
      'save' : True
    })
    pathes = server.database.pathes.PathesClass(
      logStart(_config),
      config
    )
    pathes.check()
    pathes.load()
    assert(pathes.add('test2') == '3')


def test_indexNoSave():
    config = configStart({
      'load' : False,
      'save' : False
    })
    indexes = server.database.indexes.IndexesClass(
      logStart(_config),
      config
    )
    assert(indexes.add('_') == '0')
    assert(indexes.add('test') == '1')
    assert(indexes.add('_') == '2')
    assert(indexes.add('test') == '2')

def test_indexSave():
    config = configStart({
      'index': 'indexes_test.json',
      'load' : True,
      'save' : True
    })
    indexes = server.database.indexes.IndexesClass(
      logStart(_config),
      config
    )
    indexes.check()
    assert(indexes.add('_') == '1')
    assert(indexes.add('test') == '1')
    assert(indexes.add('_') == '2')
    assert(indexes.add('test') == '2')

def test_indexSaveAndLoad():
    config = configStart({
      'index': 'indexes_test.json',
      'load' : True,
      'save' : True
    })
    indexes = server.database.indexes.IndexesClass(
      logStart(_config),
      config
    )
    indexes.check()
    indexes.load()
    assert(indexes.all('_') == ['1', '2'])
    assert(indexes.add('_') == '3')
    assert(indexes.add('test') == '3')
    assert(indexes.add('_') == '4')
    assert(indexes.add('test') == '4')

@pytest.mark.dependency()
def test_serverStart():
    """ get request  """
    global _proc
    _proc.start()
    time.sleep(1)
    assert (_proc.is_alive())


@pytest.mark.dependency(depends=["test_serverStart"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyTest():
    """ get request  """
    global _response
    headers = {'AnyServer': 'auth-test'}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStart"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyRequest():
    """ get request  """
    global _response
    headers = {'AnyServer': 'routes'}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )


@pytest.mark.dependency(depends=["test_serverStart"])
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

@pytest.mark.dependency(depends=["test_serverStart"])
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

@pytest.mark.dependency(depends=["test_serverStart"])
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

@pytest.mark.dependency(depends=["test_serverStart"])
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

@pytest.mark.dependency(depends=["test_serverStart"])
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

@pytest.mark.dependency(depends=["test_serverStart"])
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

@pytest.mark.dependency(depends=["test_serverStart"])
def test_serverSop():
    """ start server  """
    global _proc
    _proc.terminate()
    time.sleep(1)
    assert _proc.is_alive() is False

@pytest.mark.dependency()
def test_serverStartWithSave():
    """ get request  """
    global _proc
    _config = configStart({
       "log_level" : 10,
       "load" : False,
       "save" : True
    })
    _proc = multiprocessing.Process(
    target=serverStart, args=[
      logStart(_config),
      _config
    ])
    _proc.start()
    time.sleep(1)
    assert (_proc.is_alive())

@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyTestWithSave():
    """ get request  """
    global _response
    headers = {"AnyServer": "auth-test"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyRequestWithSave():
    """ get request  """
    global _response
    headers = {"AnyServer": "routes"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )


@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skipif(not test_serverStartWithSave, reason='anyserver start failed no reson to test')
def test_simpleGetWithSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skipif(not test_serverStartWithSave, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetWithSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skip(reason='incorrect implementation')
def test_simpleTestRouteGetByIdWithSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skipif(not test_serverStartWithSave, reason='anyserver start failed no reson to test')
def test_simpleTestRoutePostWithSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skipif(not test_serverStartWithSave, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetAfterPostWithSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skipif(not test_serverStartWithSave, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetByIdAfterPostWithSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skipif(not test_serverStartWithSave, reason='anyserver start failed no reson to test')
def test_serverSopWithSave():
    """ start server  """
    global _proc
    _proc.terminate()
    time.sleep(1)
    assert _proc.is_alive() is False

@pytest.mark.dependency()
def test_serverStartWithLoadAndSave():
    """ get request  """
    global _proc
    _config = configStart({
       "load" : True,
       "save" : True
    })
    _proc = multiprocessing.Process(
    target=serverStart, args=[
      logStart(_config),
      _config
    ])
    _proc.start()
    time.sleep(1)
    assert (_proc.is_alive())

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyTestWithLoadAndSave():
    """ get request  """
    global _response
    headers = {"AnyServer": "auth-test"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyRequestWithLoadAndSave():
    """ get request  """
    global _response
    headers = {"AnyServer": "routes"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )


@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skipif(not test_serverStartWithLoadAndSave, reason='anyserver start failed no reson to test')
def test_simpleGetWithLoadAndSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skipif(not test_serverStartWithLoadAndSave, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetWithLoadAndSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skip(reason='incorrect implementation')
def test_simpleTestRouteGetByIdWithLoadAndSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skipif(not test_serverStartWithLoadAndSave, reason='anyserver start failed no reson to test')
def test_simpleTestRoutePostWithLoadAndSave():
    """ post test route request  """
    global _response
    data = {'test2': 'dorol sit amet'}
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

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skipif(not test_serverStartWithLoadAndSave, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetAfterPostWithLoadAndSave():
    """ get test route request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/test/',
    )
    assert (_response.status_code == 200)
    assert (_response.text == '[{"test": "lorem ipsum", "id": "1"}, {"test2": "dorol sit amet", "id": "2"}]')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skipif(not test_serverStartWithLoadAndSave, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetByIdAfterPostWithLoadAndSave():
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

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skipif(not test_serverStartWithLoadAndSave, reason='anyserver start failed no reson to test')
def test_serverSopWithLoadAndSave():
    """ start server  """
    global _proc
    _proc.terminate()
    time.sleep(1)
    assert _proc.is_alive() is False
