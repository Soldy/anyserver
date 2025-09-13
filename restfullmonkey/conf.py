"""
config manager
"""
import sys

def configDefault()->dict[str,str|int]:
    """"
    default config 

    :return: dict[str,str|int]:
    """
    return {
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
        'disable_id' : False,
        'id_name'    : 'id',
        'dummy_test' : 'dummy'
    }

def test(config_: dict[str,str])->dict[str,str]:
    """
    config processor for test

    :param: dict[str,str]
    :return: dict[str,str]
    """
    return {**configDefault(), **config_}

def confInit (args, logging_)->dict[str,str]:
    """
    config processor

    :param: args
    :param: logging
    :return: dict[str,str]
    """

    out = configDefault()
    if int(str(int(args.port))) != args.port:
        logging_.critical('invalid port')
        sys.exit(2)
    if args.port > 65535:
        logging_.critical('invalid port to big number')
        sys.exit(2)
    if args.port < 1:
        logging_.critical('invalid port to low number')
        sys.exit(2)
    if int(str(int(args.log_level))) != args.log_level:
        logging_.critical('invalid log level')
        sys.exit(2)
    if args.log_level > 50:
        logging_.critical('invalid log level to big number')
        sys.exit(2)
    if args.log_level < 10:
        logging_.critical('invalid log level low number')
        sys.exit(2)

    out['port'] = int(args.port)
    out['log_level'] = int(args.log_level)
    out['store_type'] = args.store_type
    out['host'] = args.host
    out['db_dir'] = args.db_dir
    out['dbm_dir'] = args.dbm_dir
    out['index'] = args.index_file
    out['dbm_index'] = args.dbm_index
    out['path'] = args.path_file
    out['dbm_path'] = args.dbm_path
    if args.load is False:
        out['load'] = False
    if args.save is False:
        out['save'] = False
    if args.disable_id is False:
        out['disable_id'] = False
    out['id_name'] = args.id_name
    if args.vv:
        out['log_level'] = 10
    return out
