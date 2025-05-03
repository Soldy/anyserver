
import logging

"""
log init

:param: dict[str,str]
"""
def logStart (config_: dict[str,str])->logging:
    logging.basicConfig(
      format='%(asctime)s - %(levelname)s - %(message)s',
      level=config_['log_level']
    )
    return logging
