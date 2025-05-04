"""
cli admin args
"""
import json
from arg import parser
import pathes
import log
import conf
from databasejson import DatabasesJsonClass

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


def reversPath (path_: str)->str:
    """
    :param: str
    :return: str
    """
    return path_.replace("_", "/")


if __name__ == "__main__":
    args = parser.parse_args()
    _config = conf.start(
      args,
      log.logging,
    )
    log.start(
      _config
    )
    if args.count:
        db = DatabasesJsonClass(
          log.logging, _config)
        if args.path == '':
            print(str(db.countAll()))
        else :
            print(str(db.count(args.path)))
    if args.list_paths :
        pathes = pathes.PathesClass(
          log.logging, _config)
        pathes.load()
        list_path = pathes.all()
        for i in list_path:
            print(
              str(list_path[i])+
              " - "+
             reversPath(str(i))
            )
    if args.list_columns :
        db = DatabasesJsonClass(
          log.logging, _config)
        if args.path != '':
            columns = db.columns(args.path)
            print(
              json.dumps(columns)
            )
    if args.show_column :
        db = DatabasesJsonClass(
          log.logging, _config)
        if args.path != '' and args.column != '':
            columns = db.columnShow(args.path, args.column)
            print(
              json.dumps(columns)
            )
