
"""
" pytest
"""
import os
import time
import pytest
import requests
from threading import Thread
import multiprocessing
from restfullmonkey.log import logInit
from restfullmonkey.conf import test as configTest
from restfullmonkey.pathes import PathesClass
from restfullmonkey.pathesdbm import PathesDbmClass
from restfullmonkey.indexes import IndexesClass
from restfullmonkey.indexesdbm import IndexesDbmClass
from restfullmonkey.databasehelp import DatabaseHelpClass
from restfullmonkey.database import DatabasesClass
from restfullmonkey.server import serverStart
#import .server

_ob = {}
def configStart(config_):
  return configTest({**({
    'db_dir'   : 'db_test',
    'path'     : 'pathes_test.json',
    'index'    : 'indexes_test.json',
    'dbm_dir'  : 'dbm_test',
    'dbm_path' : 'pathes_test.dbm',
    'dbm_index': 'indexes_test.dbm',
    'save'     : False,
    'load'     : False
}), **config_})

_config = configStart({})


_proc = multiprocessing.Process(
   target=serverStart, args=[
     logInit(_config),
     _config
])
_auth_key = ''
_response = ''


"""
standard file system clean up
"""
def cleanUp():
    try:
        for i in os.listdir('db_test'):
            os.remove('db_test/'+i)
    except Exception:
        print()
    try:
        for i in os.listdir('dbm_test'):
            os.remove('dbm_test/'+i)
    except Exception:
        print()
    try:
        os.rmdir('db_test')
    except Exception:
        print()
    try:
        os.rmdir('dbm_test')
    except Exception:
        print()
    try:
        os.remove('pathes_test.json')
    except Exception:
        print()
    try:
        os.remove('indexes_test.json')
    except Exception:
        print()
    try:
        os.remove('pathes_test.dbm')
    except Exception:
        print()
    try:
        os.remove('indexes_test.dbm')
    except Exception:
        print()

def procStart(config_: dict[str,str])->bool:
    """
    standard multi process server start

    :param: dict[str,str]
    :return: bool : is a live result
    """
    global _proc
    _config = configStart(config_)
    _proc = multiprocessing.Process(
      target=serverStart, args=[
        logInit(_config),
        _config
    ])
    _proc.start()
    time.sleep(0.1)
    return _proc.is_alive()

def procTerminate():
    """
    standard multi process server stop

    :return: multiprocessing.Process
    """
    global _proc
    try:
        _proc.terminate()
    except Exception:
        return _proc
    time.sleep(0.01)
    return _proc

def helperDefination(class_, config_):
    config = configStart(config_)
    helper = class_(
      logInit(config),
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
    config = configTest({
      'load' : False,
      'save' : True
    })
    assert (config['load'] == False)
    assert (config['save'] == True)
    assert (config['dummy_test'] == 'dummy')


def test_configAgain():
    config = configTest({
      'load' : True,
      'save' : False,
      'dummy_test' : 'd2ummy'
    })
    assert (config['load'] == True)
    assert (config['save'] == False)
    assert (config['dummy_test'] == 'd2ummy')

def test_pathNoSave():
    pathes = helperDefination(
      PathesClass,
      configStart({})
    )
    assert(pathes.add('_') == '1')
    assert(pathes.add('test') == '2')

def test_pathSave():
    pathes = helperDefination(
      PathesClass,
      configStart({'save' : True})
    )
    assert(pathes.add('_') == '1')
    assert(pathes.add('test') == '2')


def test_pathSaveAndLoad():
    pathes = helperDefination(
      PathesClass,
      configStart({'load':True,'save' : True})
    )
    assert(pathes.add('test2') == '3')

def test_pathDbm():
    pathes = helperDefination(
      PathesDbmClass,
      configStart({})
    )
    assert(pathes.all() == {})
    assert(pathes.get('_') == '-1')
    assert(pathes.add('_') == '1' )
    assert(pathes.add('_') == '1' )
    assert(pathes.get('_') == '1')
    assert(pathes.all() == {'_': '1'})
    assert(pathes.get('test') == '-1')
    assert(pathes.add('test') == '2')
    assert(pathes.add('test') == '2')
    assert(pathes.get('test') == '2')
    assert(pathes.all() == {'_': '1','test':'2'})

def test_indexNoSave():
    indexes = helperDefination(
      IndexesClass,
      configStart({})
    )
    assert(indexes.add('_') == '1')
    assert(indexes.add('test') == '1')
    assert(indexes.add('_') == '2')
    assert(indexes.add('test') == '2')

def test_indexSave():
    indexes = helperDefination(
      IndexesClass,
      configStart({'save' : True})
    )
    assert(indexes.add('_') == '1')
    assert(indexes.add('test') == '1')
    assert(indexes.add('_') == '2')
    assert(indexes.add('test') == '2')

def test_indexSaveAndLoad():
    indexes = helperDefination(
      IndexesClass,
      configStart({'load':True,'save' : True})
    )
    assert(indexes.all('_') == ['1', '2'])
    assert(indexes.add('_') == '3')
    assert(indexes.add('test') == '3')
    assert(indexes.add('_') == '4')
    assert(indexes.add('test') == '4')

def test_indexDbm():
    indexes = helperDefination(
      IndexesDbmClass,
      configStart({})
    )
    assert(indexes.all('_') == [])
    assert(indexes.add('_') == '1')
    assert(indexes.add('test') == '1')
    assert(indexes.add('_') == '2')
    assert(indexes.add('test') == '2')
    assert(indexes.all('_') == ['1', '2'])

def test_databaseHelperPathFix():
    helper = DatabaseHelpClass(
      logInit(configStart({})),
      configStart({})
    )
    assert(helper.pathFix('/') == '_')
    assert(helper.pathFix('/test') == '_test')

def test_databaseHelperDataHandler():
    helper = DatabaseHelpClass(
      logInit(configStart({})),
      configStart({})
    )
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
      DatabasesClass,
      {
        'store_type': 'json',
        'load'      : False,
        'save'      : False
    })
    assert(database.post('/',{'dummy':'data'}) == 0)
    assert(database.get('/',{}) == [{'dummy': 'data', 'id': '1'}] )
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data', 'id': '1'},
    ] )
    assert(database.get('/',{'id':'1'}) == [{'dummy': 'data', 'id': '1'}] )
    assert(database.get('/',{'id':'0'}) == [] )
    assert(database.get('/test', {}) == {} )

def test_databaseNoSaveIdName():
    database = helperDefination(
      DatabasesClass,
      {
        'store_type': 'json',
        'load'      : False,
        'save'      : False,
        'id_name'   : 'newid'
    })
    assert(database.post('/',{'dummy':'data'}) == 0)
    assert(database.get('/',{}) == [{'dummy': 'data', 'newid': '1'}] )
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data', 'newid': '1'},
    ] )
    assert(database.get('/',{'newid':'1'}) == [{'dummy': 'data', 'newid': '1'}] )
    assert(database.get('/',{'newid':'0'}) == [] )
    assert(database.get('/test', {}) == {} )

def test_databaseNoSaveNoId():
    database = helperDefination(
      DatabasesClass,
      {
        'store_type': 'json',
        'load'      : False,
        'save'      : False,
        'disable_id': True
    })
    assert(database.post('/',{'dummy':'data'}) == 0)
    assert(database.get('/',{}) == [{'dummy': 'data'}] )
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data'},
    ] )
    assert(database.get('/',{'id':'1'}) == [{'dummy': 'data'}] )
    assert(database.get('/',{'id':'0'}) == [] )
    assert(database.get('/test', {}) == {} )

def test_databaseSave():
    database = helperDefination(
      DatabasesClass,
      {
        'store_type': 'json',
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
      DatabasesClass,
      {

        'store_type': 'json',
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

def test_databaseSaveIdName():
    cleanUp()
    database = helperDefination(
      DatabasesClass,
      {
        'store_type': 'json',
        'db_dir'  : 'db_test',
        'path'    : 'pathes_test.json',
        'index'   : 'indexes_test.json',
        'id_name' : 'newid',
        'load'    : False,
        'save'    : True
    })
    assert(database.post('/',{'dummy':'data'}) == 0)
    assert(database.get('/',{}) == [{'dummy': 'data', 'newid': '1'}] )
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data', 'newid': '1'},
    ] )
    assert(database.get('/',{'newid':'1'}) == [{'dummy': 'data', 'newid': '1'}] )
    assert(database.get('/',{'newid':'0'}) == [] )
    assert(database.get('/test', {}) == {} )

def test_databaseSaveAndLoadIdName():
    database = helperDefination(
      DatabasesClass,
      {

        'store_type': 'json',
        'db_dir' : 'db_test',
        'path'   : 'pathes_test.json',
        'index'  : 'indexes_test.json',
        'id_name' : 'newid',
        'load' : True,
        'save' : True
    })
    assert(database.get('/',{'newid':'0'}) == [] )
    assert(database.get('/',{'newid':'1'}) == [
      {'dummy': 'data', 'newid': '1'}])
    assert(database.post('/',{'dummy':'data plus'}) == 0)
    assert(database.get('/',{}) == [
      {'dummy': 'data', 'newid': '1'},
      {'dummy': 'data plus', 'newid': '2'}
    ])
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data', 'newid': '1'},
      {'dummy': 'data plus', 'newid': '2'}
    ])
    assert(database.get('/',{'dummy':['data plus']}) == [
      {'dummy': 'data plus', 'newid': '2'}
    ])
    assert(database.get('/',{'newid':'2'}) == [
      {'dummy': 'data plus', 'newid': '2'}])
    assert(database.get('/test', {}) == {} )

def test_databaseDbm():
    cleanUp()
    database = helperDefination(
      DatabasesClass,
      {
        'store_type': 'dbm'
      }
    )
    assert(database.post('/',{'dummy':'data'}) == 0)
    assert(database.get('/',{}) == [{'dummy': 'data', 'id': '1'}] )
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data', 'id': '1'},
    ] )
    assert(database.get('/',{'id':'1'}) == [{'dummy': 'data', 'id': '1'}] )
    assert(database.get('/',{'id':'0'}) == [] )
    assert(database.get('/test', {}) == {} )

def test_databaseDbmAgain():
    database = helperDefination(
      DatabasesClass,
      {
        'store_type': 'dbm',
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

def test_databaseDbmNoId():
    cleanUp()
    database = helperDefination(
      DatabasesClass,
      {
        'store_type': 'dbm',
        'disable_id': True
      }
    )
    assert(database.post('/',{'dummy':'data'}) == 0)
    assert(database.get('/',{}) == [{'dummy': 'data'}] )
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data'},
    ] )
    assert(database.get('/',{'id':'1'}) == [{'dummy': 'data'}] )
    assert(database.get('/',{'id':'0'}) == [] )
    assert(database.get('/test', {}) == {} )

def test_databaseDbmIdName():
    cleanUp()
    database = helperDefination(
      DatabasesClass,
      {
        'store_type': 'dbm',
        'id_name'   : 'newid'
      }
    )
    assert(database.post('/',{'dummy':'data'}) == 0)
    assert(database.get('/',{}) == [{'dummy': 'data', 'newid': '1'}] )
    assert(database.get('/',{'dummy':['data']}) == [
      {'dummy': 'data', 'newid': '1'},
    ] )
    assert(database.get('/',{'newid':'1'}) == [{'dummy': 'data', 'newid': '1'}] )
    assert(database.get('/',{'newid':'0'}) == [] )
    assert(database.get('/test', {}) == {} )

@pytest.mark.dependency()
def test_serverStart():
    """ get request  """
    assert (procStart({}))


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
def test_simpleTestRoutePostOtherPath():
    """ post test route request  """
    global _response
    data = {'test': 'lorem ipsum'}
    _response = requests.post(
      'http://localhost:8008/test2/',
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
def test_simpleTestRouteGetAfterPostOtherPath():
    """ get test route request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/test2/',
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
def test_serverStop():
    """ start server  """
    assert procTerminate().is_alive() is False

@pytest.mark.dependency()
def test_serverStartWithSave():
    """ get request  """
    cleanUp()
    assert (procStart({'save':True}))

@pytest.mark.dependency(depends=["test_serverStartWithSave"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyTestWithSave():
    """ get request  """
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
def test_simpleTestRoutePostOtherPathSave():
    """ post test route request  """
    global _response
    data = {'test': 'lorem ipsum'}
    _response = requests.post(
      'http://localhost:8008/test2/',
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
def test_simpleTestRouteGetAfterPostOtherPathWithSave():
    """ get test route request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/test2/',
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
def test_serverStopWithSave():
    """ start server  """
    assert procTerminate().is_alive() is False

@pytest.mark.dependency()
def test_serverStartWithLoadAndSave():
    """ get request  """
    assert (procStart({'load':True,'save':True}))

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyTestWithLoadAndSave():
    """ get request  """
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
    _response = requests.get(
      'http://localhost:8008/test/',
    )
    assert (_response.status_code == 200)
    assert (_response.text == 
      '[{"test": "lorem ipsum", "id": "1"}, {"test2": "dorol sit amet", "id": "2"}]'
    )
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skipif(not test_serverStartWithLoadAndSave, reason='anyserver start failed no reson to test')
def test_simpleTestRoutePostOtherPathWithLoadAndSave():
    """ post test route request  """
    global _response
    data = {'test': 'lorem ipsum'}
    _response = requests.post(
      'http://localhost:8008/test2/',
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
def test_simpleTestRouteGetAfterPostOtherPathWithLoadAndSave():
    """ get test route request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/test2/',
    )
    assert (_response.status_code == 200)
    assert (_response.text ==
      '[{"test": "lorem ipsum", "id": "1"}, {"test": "lorem ipsum", "id": "2"}]')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartWithLoadAndSave"])
@pytest.mark.skipif(not test_serverStartWithLoadAndSave, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetByIdAfterPostWithLoadAndSave():
    """ get test by id request  """
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
def test_serverStopWithLoadAndSave():
    """ start server  """
    assert procTerminate().is_alive() is False

@pytest.mark.dependency()
def test_serverDbmStart():
    """ get request  """
    assert (procStart({'store_type':'dbm'}))
    time.sleep(1)

@pytest.mark.dependency(depends=["test_serverDbmStart"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyRequestDbm():
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


@pytest.mark.dependency(depends=["test_serverDbmStart"])
@pytest.mark.skipif(not test_serverDbmStart, reason='anyserver start failed no reson to test')
def test_simpleGetDbm():
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

@pytest.mark.dependency(depends=["test_serverDbmStart"])
@pytest.mark.skipif(not test_serverDbmStart, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetDbm():
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

@pytest.mark.dependency(depends=["test_serverDbmStart"])
@pytest.mark.skip(reason='incorrect implementation')
def test_simpleTestRouteGetByIdDbm():
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

@pytest.mark.dependency(depends=["test_serverDbmStart"])
@pytest.mark.skipif(not test_serverDbmStart, reason='anyserver start failed no reson to test')
def test_simpleTestRoutePostDbm():
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

@pytest.mark.dependency(depends=["test_serverDbmStart"])
@pytest.mark.skipif(not test_serverDbmStart, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetAfterPostDbm():
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

@pytest.mark.dependency(depends=["test_serverDbmStart"])
@pytest.mark.skipif(not test_serverDbmStart, reason='anyserver start failed no reson to test')
def test_simpleTestRoutePostOtherPathDbm():
    """ post test route request  """
    global _response
    data = {'test': 'lorem ipsum'}
    _response = requests.post(
      'http://localhost:8008/test2/',
      json = data
    )
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverDbmStart"])
@pytest.mark.skipif(not test_serverDbmStart, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetAfterPostOtherPathDbm():
    """ get test route request  """
    global _response
    _response = requests.get(
      'http://localhost:8008/test2/',
    )
    assert (_response.status_code == 200)
    assert (_response.text == '[{"test": "lorem ipsum", "id": "1"}]')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverDbmStart"])
@pytest.mark.skipif(not test_serverDbmStart, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetByIdAfterPostDbm():
    """ get test by id request  """
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

@pytest.mark.dependency(depends=["test_serverDbmStart"])
def test_serverDbmStop():
    """ start server  """
    assert procTerminate().is_alive() is False
    time.sleep(1)

@pytest.mark.dependency()
def test_serverStartDbmAgain():
    """ get request  """
    assert (procStart({'store_type':'dbm'}))
    time.sleep(1)


@pytest.mark.dependency(depends=["test_serverStartDbmAgain"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyTestDbmAgain():
    """ get request  """
    headers = {"AnyServer": "auth-test"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartDbmAgain"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyRequestDbmAgain():
    """ get request  """
    headers = {"AnyServer": "routes"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )


@pytest.mark.dependency(depends=["test_serverStartDbmAgain"])
@pytest.mark.skipif(not test_serverStartDbmAgain, reason='anyserver start failed no reson to test')
def test_simpleGetDbmAgain():
    """ get request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmAgain"])
@pytest.mark.skipif(not test_serverStartDbmAgain, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetDbmAgain():
    """ get test request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmAgain"])
@pytest.mark.skip(reason='incorrect implementation')
def test_simpleTestRouteGetByIdDbmAgain():
    """ get test by id request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmAgain"])
@pytest.mark.skipif(not test_serverStartDbmAgain, reason='anyserver start failed no reson to test')
def test_simpleTestRoutePostDbmAgain():
    """ post test route request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmAgain"])
@pytest.mark.skipif(not test_serverStartDbmAgain, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetAfterPostDbmAgain():
    """ get test route request  """
    _response = requests.get(
      'http://localhost:8008/test/',
    )
    assert (_response.status_code == 200)
    assert (_response.text == 
      '[{"test": "lorem ipsum", "id": "1"}, {"test2": "dorol sit amet", "id": "2"}]'
    )
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartDbmAgain"])
@pytest.mark.skipif(not test_serverStartDbmAgain, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetByIdAfterPostDbmAgain():
    """ get test by id request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmAgain"])
@pytest.mark.skipif(not test_serverStartDbmAgain, reason='anyserver start failed no reson to test')
def test_serverStopDbmAgain():
    """ start server  """
    assert procTerminate().is_alive() is False

@pytest.mark.dependency()
def test_serverStartDbmIdName():
    """ get request  """
    cleanUp()
    assert (procStart({
      'store_type' : 'dbm',
      'id_name'    : 'newid'
    }))
    time.sleep(1)


@pytest.mark.dependency(depends=["test_serverStartDbmIdName"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyTestDbmIdName():
    """ get request  """
    headers = {"AnyServer": "auth-test"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartDbmIdName"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyRequestDbmIdName():
    """ get request  """
    headers = {"AnyServer": "routes"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )


@pytest.mark.dependency(depends=["test_serverStartDbmIdName"])
@pytest.mark.skipif(not test_serverStartDbmIdName, reason='anyserver start failed no reson to test')
def test_simpleGetDbmIdName():
    """ get request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmIdName"])
@pytest.mark.skipif(not test_serverStartDbmIdName, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetDbmIdName():
    """ get test request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmIdName"])
@pytest.mark.skip(reason='incorrect implementation')
def test_simpleTestRouteGetByIdDbmIdName():
    """ get test by id request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmIdName"])
@pytest.mark.skipif(not test_serverStartDbmIdName, reason='anyserver start failed no reson to test')
def test_simpleTestRoutePostDbmIdName():
    """ post test route request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmIdName"])
@pytest.mark.skipif(not test_serverStartDbmIdName, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetAfterPostDbmIdName():
    """ get test route request  """
    _response = requests.get(
      'http://localhost:8008/test/',
    )
    assert (_response.status_code == 200)
    assert (_response.text == 
      '[{"test": "lorem ipsum", "newid": "1"}]'
    )
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartDbmIdName"])
@pytest.mark.skipif(not test_serverStartDbmIdName, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetByIdAfterPostDbmIdName():
    """ get test by id request  """
    _response = requests.get(
      'http://localhost:8008/test/?newid=1'
    )
    assert (_response.status_code == 200)
    assert (_response.text == '[{"test": "lorem ipsum", "newid": "1"}]')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartDbmIdName"])
@pytest.mark.skipif(not test_serverStartDbmIdName, reason='anyserver start failed no reson to test')
def test_serverStopDbmIdName():
    """ start server  """
    assert procTerminate().is_alive() is False

##########################

@pytest.mark.dependency()
def test_serverStartDbmAgainIdName():
    """ get request  """
    assert (procStart({
      'store_type' : 'dbm',
      'id_name'    : 'newid'
    }))
    time.sleep(1)


@pytest.mark.dependency(depends=["test_serverStartDbmAgainIdName"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyTestDbmAgainIdName():
    """ get request  """
    headers = {"AnyServer": "auth-test"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartDbmAgainIdName"])
@pytest.mark.skip(reason='not implemented yet')
def test_keyRequestDbmAgainIdName():
    """ get request  """
    headers = {"AnyServer": "routes"}
    _response = requestGet('/',headers)
    assert (_response.status_code == 200)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )


@pytest.mark.dependency(depends=["test_serverStartDbmAgainIdName"])
@pytest.mark.skipif(not test_serverStartDbmAgainIdName, reason='anyserver start failed no reson to test')
def test_simpleGetDbmAgainIdName():
    """ get request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmAgainIdName"])
@pytest.mark.skipif(not test_serverStartDbmAgainIdName, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetDbmAgainIdName():
    """ get test request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmAgainIdName"])
@pytest.mark.skip(reason='incorrect implementation')
def test_simpleTestRouteGetByIdDbmAgainIdName():
    """ get test by id request  """
    _response = requests.get(
      'http://localhost:8008/test?newid=1'
    )
    assert (_response.status_code == 404)
    assert (_response.text == '{}')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartDbmAgainIdName"])
@pytest.mark.skipif(not test_serverStartDbmAgainIdName, reason='anyserver start failed no reson to test')
def test_simpleTestRoutePostDbmAgainIdName():
    """ post test route request  """
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

@pytest.mark.dependency(depends=["test_serverStartDbmAgainIdName"])
@pytest.mark.skipif(not test_serverStartDbmAgainIdName, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetAfterPostDbmAgainIdName():
    """ get test route request  """
    _response = requests.get(
      'http://localhost:8008/test/',
    )
    assert (_response.status_code == 200)
    assert (_response.text == 
      '[{"test": "lorem ipsum", "newid": "1"}, {"test2": "dorol sit amet", "newid": "2"}]'
    )
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartDbmAgainIdName"])
@pytest.mark.skipif(not test_serverStartDbmAgainIdName, reason='anyserver start failed no reson to test')
def test_simpleTestRouteGetByIdAfterPostDbmAgainIdName():
    """ get test by id request  """
    _response = requests.get(
      'http://localhost:8008/test/?newid=1'
    )
    assert (_response.status_code == 200)
    assert (_response.text == '[{"test": "lorem ipsum", "newid": "1"}]')
    assert (
      _response.headers['content-type']
      ==
      'application/json; charset=utf8'
    )

@pytest.mark.dependency(depends=["test_serverStartDbmAgainIdName"])
@pytest.mark.skipif(not test_serverStartDbmAgainIdName, reason='anyserver start failed no reson to test')
def test_serverStopDbmAgainIdName():
    """ start server  """
    assert procTerminate().is_alive() is False



def test_cleanUp():
    cleanUp()
