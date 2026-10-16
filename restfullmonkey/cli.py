"""
cli admin args
"""
from restfullmonkey.command import  CommandClass
from restfullmonkey.arg import parser
from restfullmonkey.outformat import OutFormat

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


if __name__ == "__main__":
    command = CommandClass()
    args = command.args()
    outFormat = OutFormat(args.text_format)
    if args.count:
        if args.path == '':
            outFormat.print(
              command.countAll()
            )
        else:
            outFormat.print(
              command.count(args.path)
            )
    elif args.list_paths :
        outFormat.print(
          command.pathList()
        )
    elif args.list_columns :
        if args.path != '':
            outFormat.print(
              command.columnsList(
                args.path
              )
            )
    elif args.show_column :
        if args.path != '' and args.column != '':
            outFormat.print(
              command.columnShow(
                args.path,
                args.column
              )
            )
