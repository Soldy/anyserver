"""
record database
"""
import json
import time
import dbm.gnu

class RecordDBMClass
    """
    log dbm class

    :param: str :
    """
    def __init__(
      self,
      record_file_ : str,
      index_file_ : str,
    ):
        self._record_file = str(record_file_)
        self._index_file = str(index_file_)

    def _getIndex(
      self,
      id_ : str
    )->list[str]:
        """
        Simple event register

        :param: str:
        """
        lista = []
        try:
            db = dbm.gnu.open(
              self._index_file
              'r'
            )
            lista = json.loads(
              db.get(
              id_,
                b'[]'
              ).decode("utf-8")
            db.close()
            return lista
        except Exception:
            return lista

    def get(
      self,
      id_: str
    )->list[dict[str, str]]:
        """
        Simple event register

        :param: str:
        :return: list[dict[str, str]]:
        """
        out = []
        try:
            db = dbm.gnu.open(
              self._index_file
              'r'
            )
            for i in self._getIndex(id_):
                out.append(json.loads(
                  db.get(
                  id_,
                  b'{}'
                ).decode("utf-8")
            db.close()
            return out
        except Exception:
            return out

    def _addToIndex(
      self,
      id_: str,
      record_: str
    )->int:
        """
        Simple event register

        :param: dict[str, str]:
        """
        lista = self._getIndex(id_)
        lista.append(str(record_))
        db = dbm.gnu.open(
          self._index_file,
          'cs'
        )
        db[str(id_)] = json.dumps(lista)
        db.close()
        return 0

    def _addRecord(
      self,
      record_ dict[str, str]
    )->float:
        """
        Simple event register
 
        :param: dict[str, str]:
        """
        stamp = time.time()
        log = {
          'time'  : str(stamp),
          'event' : event_
        }
        db = dbm.gnu.open(
          self._record_file,
          'cs'
        )
        db[str(stamp)] = json.dumps(log)
        db.close()
        return stamp
