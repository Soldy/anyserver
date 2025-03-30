import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port",
  type=int,
  dest="port",
  help="listen port",
  metavar="PORT",
  default="8008")
parser.add_argument("-l", "--host",
  type=str,
  dest="host",
  help="listen host",
  metavar="HOST",
  default="localhost"
)
parser.add_argument("--db_dir",
  type=str,
  dest="db_dir",
  help="data collection directory",
  metavar="DB",
  default="db"
)
parser.add_argument("--index_file",
  type=str,
  dest="index_file",
  help="index collection",
  metavar="INDEXFILE",
  default="indexes.json"
)
parser.add_argument("--path_file",
  type=str,
  dest="path_file",
  help="url path collection file",
  metavar="PATHFILE",
  default="pathes.json"
)
parser.add_argument("--save",
  dest="save",
  help="save the datacollection",
  action='store_false'
)
parser.add_argument("--load",
  dest="load",
  help="load the datacollection at the start",
  action='store_false'
)
parser.add_argument("--log_level",
  type=int,
  dest="log_level",
  help="log level 10 - 50",
  metavar="LOG_LEVEL",
  default="50")
parser.add_argument("--vv",
  dest="vv",
  help="Verbose log equal with --log_level 10",
  action='store_true'
)
