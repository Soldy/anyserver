
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

_ob = {}
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

def helperDefination(class_, config_):
    config = configStart(config_)
    helper = class_(
      logStart(config),
      config
    )
    helper.check()
    return helper

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
    pathes = helperDefination(
      server.database.pathes.PathesClass,
      {
        'load' : False,
        'save' : False,
      }
    )
    assert(pathes.add('_') == '1')
    assert(pathes.add('test') == '2')

def test_pathSave():
    pathes = helperDefination(
      server.database.pathes.PathesClass,
      {
        'path' : 'pathes_test.json',
        'load' : False,
        'save' : True
      }
    )
    assert(pathes.add('_') == '1')
    assert(pathes.add('test') == '2')

def test_pathSaveAndLoad():
    pathes = helperDefination(
      server.database.pathes.PathesClass,
      {
        'path' : 'pathes_test.json',
        'load' : True,
        'save' : True
      }
    )
    assert(pathes.add('test2') == '3')


def test_indexNoSave():
    indexes = helperDefination(
      server.database.indexes.IndexesClass,
      {
        'load' : False,
        'save' : False
      }
    )
    assert(indexes.add('_') == '1')
    assert(indexes.add('test') == '1')
    assert(indexes.add('_') == '2')
    assert(indexes.add('test') == '2')

def test_indexSave():
    indexes = helperDefination(
      server.database.indexes.IndexesClass,
      {
        'index': 'indexes_test.json',
        'load' : False,
        'save' : True
      }
    )
    assert(indexes.add('_') == '1')
    assert(indexes.add('test') == '1')
    assert(indexes.add('_') == '2')
    assert(indexes.add('test') == '2')

def test_indexSaveAndLoad():
    indexes = helperDefination(
      server.database.indexes.IndexesClass,
      {
        'index': 'indexes_test.json',
        'load' : True,
        'save' : True
      }
    )
    assert(indexes.all('_') == ['1', '2'])
    assert(indexes.add('_') == '3')
    assert(indexes.add('test') == '3')
    assert(indexes.add('_') == '4')
    assert(indexes.add('test') == '4')


def test_databaseHelperPathFix():
    helper = server.database.DatabaseHelpClass()
    assert(helper.pathFix('/') == '_')
    assert(helper.pathFix('/test') == '_test')

def test_databaseHelperDataHandler():
    helper = server.database.DatabaseHelpClass()
    data = helper.create(1,{'dummy':'data'})
    assert(data['id'] == 1)
    assert(data['data'] == {'dummy':'data'})
    assert('created_at' in data)
    assert('changed_at' in data)
    assert(data['created_at'] == data['changed_at'])
    data_c = helper.change(data, {'dummy':'data 2'})
    assert(data_c['created_at'] is not data_c['changed_at'])
    assert(data['changed_at'] is not data_c['changed_at'])
    assert(data['created_at'] == data_c['created_at'])
    assert(data['id'] == data_c['id'])



def test_databaseNoSave():
    database = helperDefination(
      server.database.DatabasesClass,
      {
        'load' : False,
        'save' : False
    })
    assert(database.post('/',{'dummy':'data'}) == 0)
    assert(database.get('/',{}) == [{'dummy': 'data', 'id': '1'}] )
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data', 'id': '1'},
    ] )
    assert(database.get('/',{'id':'1'}) == [{'dummy': 'data', 'id': '1'}] )
    assert(database.get('/',{'id':'0'}) == [] )
    assert(database.get('/test', {}) == {} )

def test_databaseSave():
    database = helperDefination(
      server.database.DatabasesClass,
      {
        'db_dir' : 'db_test',
        'path'   : 'pathes_test.json',
        'index'  : 'indexes_test.json',
        'load' : False,
        'save' : True
    })
    assert(database.post('/',{'dummy':'data'}) == 0)
    assert(database.get('/',{}) == [{'dummy': 'data', 'id': '1'}] )
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data', 'id': '1'},
    ] )
    assert(database.get('/',{'id':'1'}) == [{'dummy': 'data', 'id': '1'}] )
    assert(database.get('/',{'id':'0'}) == [] )
    assert(database.get('/test', {}) == {} )

def test_databaseSaveAndLoad():
    database = helperDefination(
      server.database.DatabasesClass,
      {
        'db_dir' : 'db_test',
        'path'   : 'pathes_test.json',
        'index'  : 'indexes_test.json',
        'load' : True,
        'save' : True
    })
    assert(database.get('/',{'id':'0'}) == [] )
    assert(database.get('/',{'id':'1'}) == [
      {'dummy': 'data', 'id': '1'}])
    assert(database.post('/',{'dummy':'data plus'}) == 0)
    assert(database.get('/',{}) == [
      {'dummy': 'data', 'id': '1'},
      {'dummy': 'data plus', 'id': '2'}
    ])
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data', 'id': '1'},
      {'dummy': 'data plus', 'id': '2'}
    ])
    assert(database.get('/',{'dummy':['data plus']}) == [
      {'dummy': 'data plus', 'id': '2'}
    ])
    assert(database.get('/',{'id':'2'}) == [
      {'dummy': 'data plus', 'id': '2'}])
    assert(database.get('/test', {}) == {} )

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
