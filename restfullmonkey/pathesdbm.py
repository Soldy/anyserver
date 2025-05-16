"""
dbm pathes class
"""
import dbm.gnu

class PathesDbmClass:
    """
    Multipath manager class

    :param: logging :
    :param: dict[str,str] :
    """
    def __init__(self, logging_, config_):
        self._log    = logging_
        self._config = config_
        self._serial = 0
        self._db     = dbm.gnu.open(
          self._config['dbm_path'],
          'cs'
        )

    def check(self)->bool:
        """
        Path dbm check
        :return: bool : False
        """
        return False

    def get(self, path_:str)->str:
        """
        get a path id

        :param: str : path_
        :return: str
        """
        return str(int(
          self._db.get(path_, b'-1').decode("utf-8")
        ))

    def add(self, path_:str)->str:
        """
        add / generate a path id

        :param: str : path_
        :return: str
        """
        if self.get(path_) == '-1':
            self._serial = self._serial + 1
            self._db[path_] = str(self._serial)
        return self.get(path_)

    def all(self):
        """
        get all path

        :param: str : path_
        :return: str
        """
        out = {}
        key = self._db.firstkey()
        while key is not None:
            out[key.decode('utf-8')] = self._db[key].decode('utf-8')
            key = self._db.nextkey(key)
        return out
