
_config = {
    'port'       : 8008,
    'host'       : 'localhost',
    'forward'    : '',
    'db_dir'     : 'db',
    'store_type' : 'json',
    'index'      : 'indexes.json',
    'path'       : 'pathes.json',
    'dbm_path'   : 'pathes.dbm',
    'dbm_index'  : 'indexes.dbm',
    'dbm_dir'    : 'dbm',
    'log_level'  : 10,
    'load'       : True,
    'save'       : True,
    'dummy_test' : 'dummy'
}

"""
config processor for test

:param: dict[str,str]
:return: dict[str,str]
"""
def test(config_: dict[str,str])->dict[str,str]:
    global _config
    return {**_config, **config_}

"""
config processor

:return: dict[str,str]
"""
def start (args, logging_)->dict[str,str]:
    global _config
    if int(str(int(args.port))) != args.port:
       logging_.critical('invalid port')
       quit()
    if args.port > 65535:
       logging_.critical('invalid port to big number')
       quit()
    if args.port < 1:
       logging_.critical('invalid port to low number')
       quit()
    if int(str(int(args.log_level))) != args.log_level:
       logging_.critical('invalid log level')
       quit()
    if args.log_level > 50:
       logging_.critical('invalid log level to big number')
       quit()
    if args.log_level < 10:
       logging_.critical('invalid log level low number')
       quit()

    _config['port'] = int(args.port)
    _config['log_level'] = int(args.log_level)
    _config['store_type'] = args.store_type
    _config['host'] = args.host
    _config['db_dir'] = args.db_dir
    _config['dbm_dir'] = args.dbm_dir
    _config['index'] = args.index_file
    _config['dbm_index'] = args.dbm_index
    _config['path'] = args.path_file
    _config['dbm_path'] = args.dbm_path
    if args.load == False:
        _config['load'] = False
    if args.save == False:
        _config['save'] = False
    if args.vv:
        _config['log_level'] = 10
    return _config
