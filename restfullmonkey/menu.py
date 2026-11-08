"""
extreme simple menu main
"""
import curses
from argparse import Namespace
from typing import Callable
from restfullmonkey.outformat import OutFormat
from restfullmonkey.command import CommandClass
from restfullmonkey.menucurses import menuCurses, timeMessage

def main(stdscr):
    """
    temp main menu

    :param: curses.window
    """
    command : CommandClass = CommandClass()
    args : Namespace = command.args()
    outFormat : OutFormat = OutFormat(args.text_format)
    looping : bool = True
    titles : list[str] = []
    funcs : list[Callable[[],str|dict[str,str|dict[str,str]]]] = []
    menu_list : dict[str,Callable[[],str|dict[str,str|dict[str,str]]]] = {}
    def listMenu(
      list_ : list[str|dict[str,str]]
    )->str|dict[str,str]:
        """

        :return: str|dict[str,str]:
        """
        menu : list[str] = []
        for i in list_:
            if isinstance(i, dict) and 'path' in i:
                menu.append(i['path'])
            else:
                menu.append(str(i))
        selected = menuCurses(stdscr, menu)
        return menu[selected]

    def pathListMenu()->str|dict[str,str]:
        """

        :return: str|dict[str,str]:
        """
        return listMenu(
          command.pathList(),
        )

    def pathLayer(
      fun_: Callable[[list[dict[str,str]]],str|dict[str,str]]
    )->Callable[[],str|dict[str,str]]:
        """

        :param: callable[[list[dict[str,str]]],str|dict[str,str]]
        :return: callable[str|dict[str,str]]
        """
        def out()->Callable[[],str|dict[str,str]]:
            return fun_(
              pathListMenu()
            )
        return out

    menu_list = {
      "Path List" : command.pathList,
      "Path Detect" : command.pathDetect,
      "Column List" : pathLayer(command.columnsList),
      "Index List" : pathLayer(command.indexList),
      "Index List from db" : pathLayer(command.indexListFromDB),
      "Index Check" : pathLayer(command.indexCheck),
      "Count all" : command.countAll,
      "Database reorganize" : command.reorganize,
      "Database path detect" : command.fixAll,
      "Backup Move" : command.backupMove,
    }

    for k, v in menu_list.items():
        titles.append(k)
        funcs.append(v)
    titles.append("Exit")
    outFormat.setSCR(stdscr)
    # We don’t need any try-catch.
    # If the code fails, we land on the CLI with the error message.
    # That's the expectation here.
    while looping:
        selected = menuCurses(stdscr, titles)
        timeMessage(stdscr, 'processing')
        if args.oneshot:
            looping = False
        if -1 < selected <= len(funcs)-1:
            outFormat.print(
              funcs[selected]()
            )
        else :
            looping = False

if __name__ == "__main__":
    curses.wrapper(main)
