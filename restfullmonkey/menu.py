"""
extreme simple menu main
"""
import curses
from argparse import Namespace
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
    funcs : list[callable] = []
    def listMenu(
      list_ : dict[str,str]
    )->int:
        """

        :return: int
        """
        menu = []
        for i in list_:
            menu.append(i['path'])
        selected = menuCurses(stdscr, menu)
        return menu[selected]

    def pathListMenu()->int:
        """

        :return: int
        """
        return listMenu(
          command.pathList(),
    )

    def pathLayer(fun_: callable)->callable:
        """

        :param: callable
        :return: callable
        """
        def out():
            return fun_(
              pathListMenu()
            )
        return out

    menu_list : dict[str,callable] = {
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
    while looping:
        selected = menuCurses(stdscr, titles)
        timeMessage(stdscr, 'processing')
        if args.oneshot:
            looping = False
        if len(funcs)-1 >= selected:
            outFormat.print(
              funcs[selected]()
            )
        else :
            looping = False

if __name__ == "__main__":
    curses.wrapper(main)
