"""
database manager
"""
from restfullmonkey.databasehelp import DatabaseHelpClass
from restfullmonkey.databasedbm import DatabasesDbmClass
from restfullmonkey.databasejson import DatabasesJsonClass
from restfullmonkey.databaseloop import DatabasesLoopClass

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
        self._config = config_
        if config_['store_type'] == 'json':
            self._database = DatabasesJsonClass(
              logging_,
              config_
            )
        elif config_['store_type'] == 'loop':
            self._database = DatabasesLoopClass(
              logging_,
              config_
            )
        else:
            self._database = DatabasesDbmClass(
              logging_,
              config_
            )
    def pathFix(
      self,
      path_ : str
    )->str:
        """
        fix path if 

        :param: str : the record id in str
        :return: str : result code 0 ok
        """
        if self._config['store_type'] == 'loop':
            return path_
        return self._helper.pathFix(path_)

    def filtersPreparation(
      self,
      gets_ : dict[str, any]
    )->dict[str,str]:
        """
        fix path if 

        :param: str : the record id in str
        :return: str : result code 0 ok
        """
        if self._config['store_type'] == 'loop':
            return gets_
        return self._helper.filtersPreparation(gets_)

    def post(self,
      path_: str,
      data_: dict[str, str]
    )->int:
        """
        database manager post layer

        :param: str : the record id in str
        :return: int : result code 0 ok
        """
        path = self.pathFix(path_)
        out = self._database.post(path,data_)
        if out == 0:
            return {}
        return out

    def get(
      self,
      path_: str,
      gets_: dict[str,str]|dict[str,list[str]]
    ):
        """
        get request manager

        :param: str : the record id in str
        """
        path = self.pathFix(path_)
        if not self._database.checkPath(path):
            return {}
        if self._config['id_name'] in gets_ and self._config['store_type'] != 'loop':
            return self._database.getId(
              path,
              gets_[self._config['id_name']]
            )
        if gets_ == {}:
            return self._database.getAll(path)
        return self._database.getFilter(
          path,
          self.filtersPreparation(gets_)
        )
    def check(self):
        """
         Checking the file system
         for initialization.
        """
        return self._database.check()

    def columns(
      self,
      path_ : str
    )->dict[str,dict[str, int|list[str]]]:
        """
         Columns reference
         for initialization.

        :param: str :  path name 
        :return: dict[str,dict[str, int|list[str]]] :
        """
        return self._database.columns(
          self.pathFix(path_)
        )

    def columnShow(
      self,
      path_ : str,
      column_ : str
    )->dict[str,dict[str, int|list[str]]]:
        """
         Sho a column.

        :param: str :  path name 
        :param: str :  column name 
        :return: dict[str,dict[str, int|list[str]]] :
        """
        return self._database.columnShow(
          self.pathFix(path_),
          column_
        )


    def count(
      self,
      path_ : str
    )->int:
        """
         Columns reference
         for initialization.

        :param: str :  path name 
        :return: int :
        """
        return self._database.count(
          self.pathFix(path_)
        )

    def countAll(
      self,
    )->dict[str, int]:
        """
         Columns reference
         for initialization.

        :return: dict[str,int] :
        """
        return self._database.countAll()


    def migration(
      self,
      path_ : str,
      file_name_ : str,
      type_ : str = 'csv'
    )->bool:
        """

        :param: str
        :param: str
        :param: str
        :return: bool
        """
        path = self.pathFix(path_)
        if type_ == 'csv':
            return self._database.migrationToCsv(path,file_name_)
        return False
