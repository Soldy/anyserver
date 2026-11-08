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
    def columnsList()->list[str]:
        """

        :return: list[str]
        """
        return command.columnsList(
          pathListMenu()
        )

    def indexList()->list[str]:
        """

        :return: list[str]
        """
        return command.indexList(
          pathListMenu()
        )

    def indexListFromDB()->list[str]:
        """

        :return: list[str]
        """
        return command.indexListFromDB(
          pathListMenu()
        )

    def indexCheck()->str:
        """

        :return: str
        """
        return command.indexCheck(
           pathListMenu()
        )

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
    menu_list : dict[str,callable] = {
      "Path List" : command.pathList,
      "Path Detect" : command.pathDetect,
      "Column List" : columnsList,
      "Index List" : indexList,
      "Index List from db" : indexListFromDB,
      "Index Check" : indexCheck,
      "Count all" : command.countAll,
      "Database reorganize" : command.reorganize,
      "Database path detect" : command.fixAll,
      "Backup Move" : command.backupMove,
    }

    for i in menu_list:
        titles.append(i)
        funcs.append(menu_list[i])
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
