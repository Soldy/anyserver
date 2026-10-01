"""
database abstract
"""
import logging

from restfullmonkey.databasehelp import DatabaseHelpClass

class DatabasesAbstractClass:
    """
    database dbm class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(
      self,
      logging_ : logging,
      config_ : dict[str,str]
    ):
        self._log : logging = logging_
        self._config  = config_
        self._helper : DatabaseHelpClass = DatabaseHelpClass(
          self._log,
          self._config
        )

    def _columnLen(self, column_:str|int)->int:
        """

        :param: str|int :  column name
        :return: dict[str,dict[str, int|list[str]]] :
        """
        if isinstance(column_, int):
            return column_
        if isinstance(column_, float):
            return column_
        return len(column_)

    def columDetails(
      self,
      details_ : dict[str, dict[str, set[str] | int]],
      row : dict[str, str|int|float]
    )->dict[dict[str, set[str]|int]]:
        """
        :param: dict[str, dict[str, set[str] | int]]
        :param: dict[str, str|int|float]
        :return: dict[dict[str, set[str]|int]]]
        """
        for p in row:
            if p not in details_:
                details_[p] = self.columDetailCreate(
                  row[p]
                )
            else:
                details_[p] = self.columDetailUpdate(
                  details_[p],
                  row[p]
                )
        return details_

    def columDetailCreate(
      self,
      field_ : str|int|float
    )->dict[str, set[str]|int]:
        """

        :param: str|int :  column name
        :return: dict[str,dict[str, int|list[str]]] :
        """
        types  = set([str(type(field_).__name__)])
        length = self._columnLen(field_)
        str_length = len(str(field_))

        return {
          "type" : types,
          "min"  : int(length),
          "max"  : length,
          "str_min" : int(str_length),
          "str_max" : str_length
        }

    def columDetailUpdate(
      self,
      details_ : dict[str, set[str]|int],
      field_ : str|int|float
    )->dict[str, set[str]|int]:
        """
        :param: dict[str, set[str] | int]
        :param: str| int | float
        :return: dict[str, set[str] | int]
        """
        types  = str(type(field_).__name__)
        length = self._columnLen(field_)
        str_length = len(str(field_))
        details['type'].add(types)
        details['max'] = max([details['max'], int(length)])
        details['min'] = min([details['min'], length])
        details['str_max'] = max([details['str_max'], int(str_length)])
        details['str_min'] = min([details['str_min'], str_length])
        return details

    def check(self):
        """
         Checking path in db

        """
        return
    def countAll(self)->int:
        """
        :return: int : count all records
        """
        return 0
