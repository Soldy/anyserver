""""
unified database abstract
"""

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
        self._config = config_

    def reorganize(self)->None:
        """
        database reorganize abstract

        :return: str
        """

        return 'Database not require reorganization'

    def backup(self, original_ :str)->bool:
        """
        database reorganize abstract

        :param: str
        :return: bool
        """

        source : Path = Path(original_)
        if not source.is_file():
            return False
        destination = source.with_name(
          source.stem+
          "_"+
          datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%SZ")+
          source.suffix
        )
        source.rename(destination)
        return True
