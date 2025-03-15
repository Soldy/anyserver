import os
import datetime
import json
from copy import deepcopy 

def dateTimeNow()->str:
    return (
        datetime.
        datetime.
        now().
        replace(tzinfo=datetime.timezone.utc).
        isoformat()
    )

class Holder:
    def __init__(self):
         self._db = {}
         self._index = []
         self._active = []
         self._save_data = True
         self._load_data = True
         self._id = 0
         self._index_file = 'index.json'
         self._db_dir = 'db'
    def _getId(self):
        self._id = self._id + 1
        return deepcopy(self._id)
    def _copy(self, result_: list[str]):
        out = []
        for i in result_:
            if self._db[i]['is_active']:
                out.append(
                    deepcopy(
                        self._db[i]
                    )
                )
                out[len(out)-1]['is_active'] = 'true'
        return out
    def _checkAndFix(self):
         _error = False
         if not self._save_data and not _load_data:
             return 
         if not os.path.exists(self._db_dir):
             logging.info('Creating database directory')
             os.makedirs(self._db_dir)
             self._fresh_db_ = True 
         if not os.path.isdir(self._db_dir):
             logging.critical('Database directory error')
             _error = True
         if not os.path.exists(self._index_file):
             logging.info('Creating index file')
             with open(self._index_file, 'w') as file_:
                 json.dump([], file_)
             self._fresh_db_ = True 
         if not os.path.isfile(self._index_file):
             logging.critical('Index file error')
             _error = True
         if _error:
               quit()
    def _fileName(id_:str)->str:
        return (
            self._db_dir+
            '/'+
            str(id_)+
            '.json'
        )
    def _save(self, id_:str):
        if self._save_data == True:
             with open(_fileName(id_), 'w') as file_:
                  json.dump(self._data_base[id_], file_)

    def _read(self, id_:str):
        with open(self._fileName(id_), 'r') as file_:
            _data_base_[id_] = json.load(file_)
    def _readAll(self):
        for i in _index_:
            _dbRead(i)
    def all(self):
        return self._copy(self._db)
    def save(self, data_: dict[str, Any]):
        now = dateTimeNow()
        data_['id'] = self._getId()
        data_['is_active'] = True
        data_['created_at'] = deepcopy(now)
        data_['updated_at'] = deepcopy(now)
        self._db[str(_id_)] = data_
    def edit(self, data_: dict[str, Any]):
        _id = str(data_['id'])
        if 'id' not in data_:
            return
        if _id not in self._db:
            return
        if self._db[_id]['is_active'] == False:
            return
        data_['is_active'] = True
        data_['created_at'] = self._db[_id]['created_at']
        data_['updated_at'] = dateTimeNow()
        self._db[_id] = data_
    def delete(self, ids_ : list[int]):
        for i in ids_:
            if str(ids_[i]) in self._db:
                self.db[str(i)]['is_active'] = False
    def get(self, filters_: dict[str, str|int]):
        if 'id' in filters_:
            return self._do_json_response(
                _getId_(filters_['id'])
            )
        if filters_ == {}:
            return self.all()
        else:
            return self._do_json_response(
                self._filter(filters_)
            )
