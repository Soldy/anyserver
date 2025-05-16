"""
main start 
"""
import logging
from arg import parser
from log import logStart
from conf import confInit
from server import serverStart



if __name__ == "__main__":
    args = parser.parse_args()
    _config = confInit(
      args,
      logging
    )
    serverStart(
      logStart(
        _config
      ),
      _config
   )
