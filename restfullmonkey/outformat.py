"""
command line output format
"""
import json
from restfullmonkey.menucurses import printCurses, tableMake



class OutFormat:
    """
    menu function

    :param: str:
    """
    def __init__(
      self,
      format_ : str  = 'text'
    ):
        self._scr    = None
        self.setFormat(format_) # text | json

    def setSCR(
      self,
      scr_
    ):
        """
        sign the song all around
        scr set some where tick tick tack

        :param:scr_ : __curses.window
        """
        self._scr = scr_

    def setFormat(
      self,
      format_ : str = 'text'
    )->None:
        """
        format changer

        :param: str
        """
#pylint: disable=W0719
        if format_ not in ['json', 'text']:
            raise Exception('Wrong api output format')
        self._format : str = str(format_)
#pylint: enable=W0719

    def print(
      self,
      txt_ : str|list[str|dict[str, str]]
    ):
        """
        print layer

        :param: str|list[str|dict[str, str]]
        """
        if not isinstance(txt_, str):
            if self._format == 'json':
                txt_ = json.dumps(
                  txt_
                )
            else:
                txt_ = tableMake(txt_)
        if self._scr  is not None:
            return printCurses(
              self._scr,
              txt_
            )
        return print(txt_)
