"""
dbm pathes class
"""
import dbm.gnu
from pathesabstract import PathesAbstractClass

class PathesDbmClass(PathesAbstractClass):
    """
    Multipath manager class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(self, logging_, config_):
        super().__init__(logging_, config_)
        self.load()

    def check(self)->bool:
        """
        Path dbm check
        :return: bool : False
        """
        return False

    def add(self, path_:str)->str:
        """
        add / generate a path id

        :param: str : path_
        :return: str
        """
        path = super().add(path_)
        with dbm.gnu.open(
          self._config['dbm_path'],
          'cs'
        ) as db:
            db[path_] = str(path)
        return path

    def load(self)->None:
        """
        get all path

        :return: None
        """
        with dbm.gnu.open(
          self._config['dbm_path'],
          'cs'
        ) as db:
            key = db.firstkey()
            while key is not None:
                k = key.decode('utf-8')
                self._path[k] = db[key].decode('utf-8')
                if int(self._path[k]) > self._serial:
                    self._serial = int(self._path[k])
                key = db.nextkey(key)
