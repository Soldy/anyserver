"""
dbm pathes class
"""
import dbm.gnu
from restfullmonkey.pathesabstract import PathesAbstractClass

class PathesDbmClass(PathesAbstractClass):
    """
    Multipath manager for dbm

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(self, logging_, config_: str):
        super().__init__(logging_, config_)
        self.check()
    def check(self)->bool:
        """
        Path dbm check
        :return: bool : False
        """
        self._load()
        return False

    def get(self, path_:str)->str:
        """
        add / generate a path id

        :param: str : path_
        :return: str
        """
        if path_ in self._path:
            return str(self._path[path_])
        with dbm.gnu.open(
          self._config['dbm_path'],
          'cs'
        ) as db:
            db[path_] = str(self._serial)
            self._path[path_] = str(
              self._serial
            )
            self._serial += 1
        return str(self._path[path_])

    def _load(self)->None:
        """
        get all path

        :return: None
        """
        serials = []
        with dbm.gnu.open(
          self._config['dbm_path'],
          'cs'
        ) as db:
            key = db.firstkey()
            while key is not None:
                k = key.decode('utf-8')
                self._path[k] = db[key].decode('utf-8')
                serials.append(
                  int(
                    db[key].decode('utf-8')
                  )
                )
                key = db.nextkey(key)
            if len(serials) > 0:
                self._serial = int(
                  max(serials)
                )

    def reorganize(self)->None:
        """
        database gdm reorganize

        :return: str
        """

        with dbm.gnu.open(
          self._config['dbm_path'],
          'cs'
        ) as db:
            db.reorganize()
        return 'Database reorganized'
