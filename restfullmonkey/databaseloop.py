"""
dummy database
"""
from restfullmonkey.databasehelp import DatabaseHelpClass

class DatabasesLoopClass:
    """
    database dbm class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(self, logging_, config_):
        self._log     = logging_
        self._config  = config_
        self._helper = DatabaseHelpClass(
          self._log,
          self._config
        )

    def looping(
      self,
      method_,
      path_,
      data_
    )->dict[str, str]:
        """
        loop response data generator

        :param: str : path
        :param: dict[str,str] : filters
        :return: dict[str,any]
        """
        return ({
          'method' : method_,
          'path'   : path_,
          'data'   : data_
        })

    def post(self,
      path_: str,
      data_: dict[str, str]
    )->int:
        """
        Db record post

        :param: str : the record id in str
        :return: dict[str,any]
        """
        return self.looping('POST', path_, data_)


    def get(
      self,
      path_:str,
      gets_: dict[str,str]
    )->dict[str,any]:
        """
        get All record

        :param: str : path
        :return: dict[str,any]
        """
        return self.looping('GET', path_, gets_)

    def check(self):
        """
         Checking path in db

        """
        return
