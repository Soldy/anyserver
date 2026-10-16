"""
extreme simple menu main
"""
import curses
from restfullmonkey.outformat import OutFormat
from restfullmonkey.command import CommandClass
from restfullmonkey.menucurses import menuCurses


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
        selected = menuCurses(stdscr, [
          "Path list",
          "Column list",
          "Count all",
          "Exit"
        ])
        if selected == 0:
            outFormat.print(
              command.pathList()
            )
        elif selected == 2:
            outFormat.print(
              command.countAll()
            )
        elif selected == 1:
            outFormat.print(
              command.columnsList(
                pathListMenu(
                  command.pathList(),
                )
              )
            )
        else :
            looping = False
        if args.oneshot:
            looping = False

if __name__ == "__main__":
    curses.wrapper(main)
