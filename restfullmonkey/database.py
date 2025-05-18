"""
database manager
"""
from restfullmonkey.databasehelp import DatabaseHelpClass
from restfullmonkey.databasedbm import DatabasesDbmClass
from restfullmonkey.databasejson import DatabasesJsonClass

class DatabasesClass:
    """
    database manager class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(self, logging_, config_):
        self._helper = DatabaseHelpClass(
          logging_,
          config_
        )
        if config_['store_type'] == 'json':
            self._database = DatabasesJsonClass(
              logging_,
              config_
            )
        else:
            self._database = DatabasesDbmClass(
              logging_,
              config_
            )

    def post(self,
      path_: str,
      data_: dict[str, str]
    )->int:
        """
        database manager post layer

        :param: str : the record id in str
        :return: int : result code 0 ok
        """
        return self._database.post(path_,data_)
    def get(
      self,
      path_: str,
      gets_: dict[str,str]
    ):
        """
        get request manager

        :param: str : the record id in str
        """
        path = self._helper.pathFix(path_)
        if not self._database.checkPath(path):
            return {}
        if 'id' in gets_:
            return self._database.getId(path, gets_['id'])
        if gets_ == {}:
            return self._database.getAll(path)
        return self._database.getFilter(path, gets_)
    def check(self):
        """
         Checking the file system
         for initialization.
        """
        return self._database.check()
