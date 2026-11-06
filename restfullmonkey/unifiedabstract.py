""""
unified database abstract
"""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

class UnifiedAbstact:
    """
    Multipath manager class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(
      self,
      logging_,
      config_ : dict[str,str]
    ):
        self._log    = logging_
        self._config : dict[str,str] = deepcopy(config_)
        self._extension : str = 'temp'
        self._single_file : bool = True
        self._store : str = ''

    def reorganize(self)->None:
        """
        database reorganize abstract

        :return: str
        """
        return 'Database not require reorganization'

    def _backupMove(self, original_ : str = '')->bool:
        """
        database reorganize abstract

        :param: str
        :return: bool
        """
        if original_ == '':
            original_ = self._store
        if original_ == '':
            return False
        source : Path = Path(original_)
        if not source.is_file() or not source.is_dir():
            return False
        destination = source.with_name(
          source.stem+
          "_"+
          datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%SZ")+
          source.suffix
        )
        source.rename(destination)
        if source.is_dir():
            newDir = Path(original_)
            newDir.mkdir()
        return True

    def databaseFileList(self, path_ : str)->list[str]:
        """
        database file list detect

        :param: str
        :return: list[str]
        """
        if self._single_file:
            return []
        out : list[str] = []
        folder : Path = Path(path_)
        for i in folder.iterdir():
            if i.is_file() and i.suffix == ('.'+self._extension):
                out.append(str(i.stem))
        return out

    def backupMove(self)->bool:
        """
        database backup

        :return: bool
        """
        self._backupMove()
        return True
