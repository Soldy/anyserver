import os
import math
import time
import datetime
from copy import deepcopy 


class DatabaseHelpClass:
    def __init__(self):
        self._checked = False

    """
    path name fix

    :param: str : the record id in str
    :return: str: full path 
    """
    def pathFix(self, path_:str)->str:
        return path_.replace("/", "_")

    """
    check dir existance
    :param: str:
    :return: bool:
    """
    def checkDir(self, dir_:str)->bool:
        if self._checked:
           return False
        if not os.path.exists(
          dir_
        ):
            self._log.debug(
              'Creating database directory'
            )
            os.makedirs(
              dir_
            )
            time.sleep(1)
        if not os.path.isdir(
          dir_
        ):
            self._log.critical(
              'Database directory error'
            )
            return True
        self._checked = True
        return False

    """
    create data structure
    """
    def create(
      self,
      id_: int,
      data_: dict[str,any]
    )->dict[str,any]:
        time = math.floor(
          datetime.datetime.timestamp(
            datetime.datetime.now()
          )
        )
        out = {}
        out['data']       = deepcopy(data_)
        out['id']         = deepcopy(id_)
        out['created_at'] = deepcopy(time)
        out['changed_at'] = deepcopy(time)
        return out

    """
    change data structure
    """
    def change(
      self,
      data_: dict[str,any],
      record_: dict[str,any]
    )->dict[str,any]:
        record = {}
        record['id'] = data_['id']
        record['created_at'] = data_['created_at']
        time = math.floor(
          datetime.datetime.timestamp(
            datetime.datetime.now()
          )
        )
        record['data']       = {**data_['data'], **record_}
        record['changed_at'] = time
        return deepcopy(record)
    def extend(
      self,
      data_: dict[str,any],
      record_: dict[str,any]
    )->dict[str,any]:
        out = deepcopy(record_['data'])
        for i in data_:
            out[i] = data_[i]
        return self.change(out, record_)

    """
     output data format
    """
    def outdata(
      self,
      data_: dict[str,any]
    )->dict[str,any]:
        out       = deepcopy(record['data'])
        out['id'] = deepcopy(record['id'])
        return out
