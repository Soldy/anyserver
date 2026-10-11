"""
command class
"""
import json
from restfullmonkey import log
from restfullmonkey.database import DatabasesClass
from restfullmonkey.pathesjson import PathesJsonClass
from restfullmonkey.pathesdbm import PathesDbmClass
from restfullmonkey.databasehelp import DatabaseHelpClass


class CommandClass:
    """
    cli and menu command class

    :param: dict[str, str]
    """
    def __init__(
      self,
      config_ : dict[str, str|int]
    ):
        self._config = config_
        self._helper = DatabaseHelpClass(
          log.logging,
          config_
        )
        self._db : callable = DatabasesClass(
          log.logging, config_
        )

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

    def print(self, output_ : any):
        """
        simple print layer

        :param: any
        :return: None
        """
        print(output_)

    def countAll(self):
        """
        count all path

        :return: None
        """
        self.print(str(self._db.countAll()))

    def count(self, path_ : str):
        """
        count a path

        :param: str
        :return: None
        """
        self.print(str(self._db.count(path_)))

    def columnsList(self, path_ :str):
        """
        list of columns 

        :param: str
        :return: None
        """
        columns = self._db.columns(
          path_
        )
        print(json.dumps(columns))

    def columnShow(self, path_ : str, column_ : str):
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
        print(json.dumps(columns))

    def pathList(self):
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
              'id' : self._helper.pathFixReverse(str(i)),
              'path' : list_path[i]
            })
        self.print(out)
