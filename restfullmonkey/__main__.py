"""
main start 
"""
import logging
from restfullmonkey.arg import parser
from restfullmonkey.log import logInit
from restfullmonkey.conf import confInit
from restfullmonkey.server import serverStart



if __name__ == "__main__":
    args = parser.parse_args()
    _config = confInit(
      args,
      logging
    )
    serverStart(
      logInit(
        _config
      ),
      _config
   )
