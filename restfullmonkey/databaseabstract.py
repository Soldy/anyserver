"""
database abstract
"""
import logging

from collections.abc import Iterable
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

    def filterCheck(
      self,
      row_ : dict[str, str|int|float],
      filters_: dict[str, list[str]]
    )->bool:
        """
        The search filter always uses OR logic,
        not AND logic. 
        If any comparison is true comes back true.
        This is not a powerful search and is not built
        for a live server.
        Enough for a development server. Pointless to do more.

        :param: dict[str, str|int|float]
        :param: dict[str, list[str]] : filters
        :return: bool
        """
        for filter_key in filters_:
            if filter_key not in row_:
                continue
            for filter_val in filters_[filter_key]:
                if filter_val.lower() in str(row_[filter_key]).lower():
                    return True
        return False

    def _columnLen(self, column_:str|int)->int:
        """

        :param: str|int :  column name
        :return: dict[str,dict[str, int|list[str]]] :
        """
        if isinstance(column_, str):
            return len(column_)
        return column_

    def columDetails(
      self,
      details_ : dict[str, dict[str, set[str] | int]],
      row_ : dict[str, str|int|float]
    )->dict[str, dict[str, set[str]|int]]:
        """
        :param: dict[str, dict[str, set[str] | int]]
        :param: dict[str, str|int|float]
        :return: dict[str, dict[str, set[str]|int]]
        """
        if not isinstance(row_, Iterable):
           details_['0'] = self.columDetailCreate(
             row_
           )
           return details_
        for p in row_:
            if p not in details_:
                details_[p] = self.columDetailCreate(
                  row_[p]
                )
            else:
                details_[p] = self.columDetailUpdate(
                  details_[p],
                  row_[p]
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
        types  = {type(field_).__name__}
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
        details_['type'].add(types)
        # int for copy
        details_['max'] = max(details_['max'], int(length))
        details_['min'] = min(details_['min'], length)
        # swalow copy fine here created above so thats int always.
        details_['str_max'] = max(details_['str_max'], int(str_length))
        details_['str_min'] = min(details_['str_min'], str_length)
        # str_length created in this function int are not needed
        return details_

    def columDetailsToList(
      self,
      details_ : dict[str, dict[str, set[str]|int]]
    )->list[str]:
        """
        at the moment same as details_.keys() 
        latter that change

        :param: dict[str, dict[str, set[str]|int]]
        :return: list[str]
        """
        out = []
        for p in details_:
            out.append(p)
        return out

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
