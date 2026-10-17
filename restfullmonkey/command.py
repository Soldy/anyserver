"""
command class
"""
from argparse import Namespace
from restfullmonkey import log, conf
from restfullmonkey.arg import parser
from restfullmonkey.database import DatabasesClass
from restfullmonkey.pathesjson import PathesJsonClass
from restfullmonkey.pathesdbm import PathesDbmClass
from restfullmonkey.indexesjson import IndexesJsonClass
from restfullmonkey.indexesdbm import IndexesDbmClass
from restfullmonkey.databasehelp import DatabaseHelpClass


class CommandClass:
    """
    cli and menu command class

    """
    def __init__(self):
        self._args = parser.parse_args()
        self._config = conf.confInit(
          self._args,
          log.logging,
        )
        self._helper = DatabaseHelpClass(
          log.logging,
          self._config
        )
        self._db : callable = DatabasesClass(
          log.logging, self._config
        )
        self._scr : any = None

    def args(self)->Namespace:
        """
        pathes init

        :return: Namespace
        """
        return self._args

    def pathesInit(self, conf_)->callable:
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

    def indexesInit(self, conf_)->callable:
        """
        indexes init

        :return: callable
        """
        if conf_['store_type'] == 'json' :
            return IndexesJsonClass(
              log.logging, conf_
            )
        return IndexesDbmClass(
          log.logging, conf_
        )

    def countAll(self)->None:
        """
        count all path

        :return: None
        """
        return str(self._db.countAll())

    def count(self, path_ : str)->None:
        """
        count a path

        :param: str
        :return: None
        """
        return str(self._db.count(path_))

    def columnsList(self, path_ :str)->None:
        """
        list of columns 

        :param: str
        :return: None
        """
        columns = self._db.columns(
          path_
        )
        return columns

    def columnShow(self, path_ : str, column_ : str)->None:
        """
        show a column 

        :param: str
        :param: str
        :return: None
        """
        columns = self._db.columnShow(
          path_,
          column_
        )
        return columns

    def pathList(self)->None:
        """
        show a column 

        :return: None
        """
        pathes : callable = self.pathesInit(self._config)
        pathes.check()
        list_path = pathes.all()
        out = []
        for i in list_path:
            out.append({
              'id' : list_path[i],
              'path' : self._helper.pathFixReverse(str(i))
            })
        return out


    def indexListFromDB(
      self,
      path_: str
    )->None:
        """
        generate indexlist from db file

        :param: str
        :return: None
        """

        return self._db.indexList(path_)

    def indexList(
      self,
      path_: str
    )->None:
        """
        get indexlist

        :param: str
        :return: None
        """
        return self._db.indexAll(path_)
