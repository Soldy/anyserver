"""
log setup
"""
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
