"""
cli admin args
"""
import json
from restfullmonkey import log, conf
from restfullmonkey.arg import parser
from restfullmonkey.database import DatabasesClass
from restfullmonkey.pathesjson import PathesJsonClass
from restfullmonkey.pathesdbm import PathesDbmClass
from restfullmonkey.databasehelp import DatabaseHelpClass

parser.add_argument(
  "--store_type",
  dest="store_type",
  choices=["json", "dbm"],
  default="json"
)

parser.add_argument('-r', '--report',
  dest='report',
  help="short report",
  action='store_false'
)
parser.add_argument('-c', '--count',
  dest='count',
  help="count the records",
  action='store_true'
)
parser.add_argument("-lp", "--list-paths",
  dest="list_paths",
  help="list all paths",
  action='store_true'
)

parser.add_argument("-lc", "--list-columns",
  dest="list_columns",
  help="list columns in a path",
  action='store_true'
)

parser.add_argument("-sc", "--show-colum",
  dest="show_column",
  help="show column in a path",
  action='store_true'
)


parser.add_argument("-p", "--path",
  type=str,
  dest="path",
  help="path analized",
  metavar="PATH",
  default=""
)

parser.add_argument("-tc", "--column",
  type=str,
  dest="column",
  help="column",
  metavar="COLUMN",
  default=""
)

parser.add_argument("-csv", "--tocsv",
  type=str,
  dest="csv",
  help="csv",
  metavar="CSV",
  default=""
)

def pathesInit(conf_)->callable:
    """
    pathes init

    :return: callable
    """
    if conf_['store_type'] == 'json' :
        return PathesJsonClass(
          log.logging, conf_
        )
    return PathesDbmClass(
      log.logging, conf_
    )

if __name__ == "__main__":
    args = parser.parse_args()
    _config = conf.confInit(
      args,
      log.logging,
    )
    log.logInit(
      _config
    )
    helper = DatabaseHelpClass(
      log.logging,
      _config
    )
    db : callable = DatabasesClass(
      log.logging, _config
    )
    if args.count:
        if args.path == '':
            print(str(db.countAll()))
        else :
            print(str(db.count(args.path)))
    if args.list_paths :
        pathes : callable = pathesInit(_config)
        pathes.check()
        list_path = pathes.all()
        for i in list_path:
            print(
              str(list_path[i])+
              " - "+
             helper.pathFixReverse(str(i))
            )
    if args.list_columns :
        if args.path != '':
            columns = db.columns(
                args.path
            )
            print(json.dumps(columns))
    if args.show_column :
        if args.path != '' and args.column != '':
            columns = db.columnShow(
              args.path,
              args.column
            )
            print(json.dumps(columns))
