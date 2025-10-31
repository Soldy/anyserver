"""
log setup
"""
import json
import time
import dbm.gnu
import logging

def logInit (config_: dict[str,str])->logging:
    """
    log init

    :param: dict[str,str]
    """
    logging.basicConfig(
      format='%(asctime)s - %(levelname)s - %(message)s',
      level=config_['log_level']
    )
    return logging


class LogDBMClass:
    """
    log dbm class

    :param: str :
    """
    def __init__(self, log_file_ : str):
        self._log_file = str(log_file_)
    def addEvent(
      self,
      event_ : dict[str, str]
    )->int:
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
          self._log_file,
          'cs'
        )
        db[str(stamp)] = json.dumps(log)
        db.close()
        return 0
    def addEvents(
      self,
      events_ : dict[dict[str, str]]
    )->int:
        """
        Multiple event register

        :param: dict[dict[str, str]]:
        """
        for event in events_:
            self.addEvent(event)
        return 0
