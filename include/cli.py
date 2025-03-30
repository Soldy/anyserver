from arg import parser 
import pathes
import database
import log
import conf


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

parser.add_argument("-p", "--path",
  type=str,
  dest="path",
  help="path analized",
  metavar="PATH",
  default=""
)


def reversPath (path_: str)->str:
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
        db = database.DatabasesClass(
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
