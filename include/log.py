
import logging

def start (_config):
    logging.basicConfig(
      format='%(asctime)s - %(levelname)s - %(message)s',
      level=_config['log_level']
    )
    return logging
