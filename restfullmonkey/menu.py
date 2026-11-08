"""
extreme simple menu main
"""
import curses
from restfullmonkey.outformat import OutFormat
from restfullmonkey.command import CommandClass
from restfullmonkey.menucurses import menuCurses, timeMessage


def main(stdscr):
    """
    temp main menu

    :param: curses.window

    """
    command = CommandClass()
    args = command.args()
    outFormat = OutFormat()
    outFormat = OutFormat(args.text_format)
    outFormat.setSCR(stdscr)
    def columnsList()->any:
        return command.columnsList(
          pathListMenu(
            command.pathList(),
          )
        )

    def indexList()->any:
        return command.indexList(
          pathListMenu(
            command.pathList(),
          )
        )

    def indexListFromDB()->any:
        return command.indexListFromDB(
          pathListMenu(
            command.pathList(),
          )
        )

    def indexCheck()->any:
        return command.indexCheck(
           pathListMenu(
             command.pathList(),
           )
        )

    def pathListMenu(
      pathes_ : dict[str,str]
    ):
        menu = []
        for i in pathes_:
            menu.append(i['path'])
        selected = menuCurses(stdscr, menu)
        return menu[selected]

    looping = True
    while looping:
        titles = [
          "Path List",
          "Path Detect",
          "Column List",
          "Index List",
          "Index List from db",
          "Index Check",
          "Count all",
          "Database reorganize",
          "Database path detect",
          "Backup Move",
          "Exit"
        ]
        funcs = [
          command.pathList,
          command.pathDetect,
          columnsList,
          indexList,
          indexListFromDB,
          indexCheck,
          command.countAll,
          command.reorganize,
          command.fixAll,
          command.backupMove
        ]
        selected = menuCurses(stdscr, titles)
        timeMessage(stdscr, 'processing')
        if args.oneshot:
            looping = False
        if len(funcs) >= selected:
            outFormat.print(
              funcs[selected]()
            )
        else :
            looping = False

if __name__ == "__main__":
    curses.wrapper(main)
