import datetime
import math
from copy import deepcopy 


class DatabaseHelpClass:
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
    def change(
      self,
      data_: dict[str,any],
      record_: dict[str,any]
    )->dict[str,any]:
        time = math.floor(
          datetime.datetime.timestamp(
            datetime.datetime.now()
          )
        )
        record['data']       = deepcopy(data_)
        record['changed_at'] = deepcopy(time)
        return record
    def extend(
      self,
      data_: dict[str,any],
      record_: dict[str,any]
    )->dict[str,any]:
        out = deepcopy(record_['data'])
        for i in data_:
            out[i] = data_[i]
        return self.change(out, record_)
    def outdata(
      self,
      data_: dict[str,any]
    )->dict[str,any]:
        out       = deepcopy(record['data'])
        out['id'] = deepcopy(record['id'])
        return out
