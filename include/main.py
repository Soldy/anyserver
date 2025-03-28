import argparse
import server

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", dest="port",
  help="listen port", metavar="PORT", default="8008")
parser.add_argument("-l", "--host", dest="host",
  help="listen host", metavar="HOST", default="localhost")
parser.add_argument("-d", "--db", dest="db",
  help="data collection directory", metavar="DB", default="db")
parser.add_argument("--index", dest="index",
  help="index collection", metavar="INDEXFILE", default="indexes.json")
parser.add_argument("--path", dest="path",
  help="url path collection file", metavar="PATHFILE", default="pathes.json")
parser.add_argument("--save", dest="save",
  help="save the datacollection", metavar="True/False", default=True)
parser.add_argument("--load", dest="load",
  help="load the datacollection at the start", metavar="True/False", default=True)
args = parser.parse_args()

server.start(args)
