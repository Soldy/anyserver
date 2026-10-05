"""
dummy database
"""

from restfullmonkey.databaseabstract import DatabasesAbstractClass

class DatabasesLoopClass(DatabasesAbstractClass):
    """
    database dbm class

    :param: logging :
    :param: dict[str,str] :
    """

    def looping(
      self,
      path_ : str,
      data_ : dict[str,str]|list[str]|None = None,
      method_ : str = 'GET'
    )->dict[str, str]:
        """
        loop response data generator

        :param: str : path
        :param: dict[str,str]|list[str] : data
        :param: str : method
        :return: dict[str,any]
        """
        if data_ is None :
            data_ = {}
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
        return self.looping(path_, data_, 'POST')


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
        return self.looping(path_, gets_)

    def getAll(
      self,
      path_:str
    )->dict[str,any]:
        """
        get All record

        :param: str : path
        :return: dict[str,any]
        """
        return self.looping(path_)

    def getId(
      self,
      path_:str,
      gets_: list[str]
    )->dict[str,any]:
        """
        just loop back all

        :param: str : path
        :return: dict[str,any]
        """
        return self.looping(path_, gets_)

    def getFilter(
      self,
      path_:str,
      gets_: dict[str,str]
    )->dict[str,any]:
        """
        just loop back all

        :param: str : path
        :param: dict[str,str]
        :return: dict[str,any]
        """
        return self.looping(path_, gets_)

    def checkPath(
      self,
      path_: str
    )->bool:
        """
        just loop back all

        :param: str : path
        :return: bool
        """
        if isinstance(path_, str):
            return True
        return True
