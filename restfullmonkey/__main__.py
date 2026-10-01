"""
main start 
"""
import logging
import restfullmonkey.arg as parser
from restfullmonkey.conf import confInit
from restfullmonkey.server import serverStart



if __name__ == "__main__":
    parser.argServer()
    args = parser.parser.parse_args()
    _config = confInit(
      args,
      logging
    )
    serverStart(
      _config
   )
