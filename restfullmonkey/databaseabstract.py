
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

