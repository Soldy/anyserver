"""
Simplified curses menu
"""
import curses
from copy import deepcopy

def tableMake(
  rows_ : list[str|dict[str,str|int|float]]|dict[str,dict[str,str|int|float]]
)->str:
    """
    Convert a list of dictionaries into a formatted text table.

    :param: list[str|dict[str,str|int|float]]|dict[str,dict[str,str|int|float]]
    :return: str
    """

    if not rows_:
        return ""
    # fix the path dict to list
    if isinstance(rows_, dict):
        columns = []
        row_checked = []
        for i in rows_:
            newrow = {}
            newrow['name'] = str(i)
            if (
              isinstance(rows_[i], (str, int, float, bool))
            ):
                newrow['value'] = str(rows_[i])
            else :
                for a in rows_[i]:
                    newrow[a] = str(rows_[i][a])
            row_checked.append(deepcopy(newrow))
        rows_ = row_checked
    # Use dictionary keys as column nameso
    if isinstance(rows_[0], dict):
        columns = list(rows_[0].keys())
    else:
        # temp solution works but ugly
        return "\n".join(str(row)+' ' for row in rows_)


    # Calculate width for each column
    widths = {}

    for column in columns:
        values = [str(row.get(column, "")) for row in rows_]
        widths[column] = max(
            len(str(column)),
            max(len(value) for value in values)
        )

    # Create one table row
    def format_row(row):
        return " ┊ ".join(
            str(row.get(column, "")).ljust(widths[column])
            for column in columns
        )

    separator = "━╀━".join("━" * widths[column] for column in columns)

    table = [
        format_row({column: column for column in columns}),
        separator
    ]

    table.extend(format_row(row) for row in rows_)
    return "\n".join(table)


def printCurses(scr_, text_: str)->None:
    """
    menu function

    :param: __curses.window:
    :param: str:
    :return: None:
    """
    looping : bool = True
    start_pos : int = 0
    lines : list[str] = str(text_).splitlines()
    length : int = len(lines)
    height : int
    width : int
    height, width = scr_.getmaxyx()
    height = height - 1
    def printRender():
        end : int = int(height)
        scr_.clear()
        if (start_pos + height - 2) > length:
            end = length - start_pos
        for i in range(end):
            line : int = i+start_pos
            if  length > line:
                scr_.addnstr(i, 0, lines[line], width - 1)
        scr_.addnstr(height, 10, 'Press space key to continue', width - 1)
        scr_.refresh()
    while looping:
        printRender()
        key = scr_.getch()
        if key == ord(" "):
            looping = False
        elif key == curses.KEY_DOWN:
            if length > (start_pos + height - 2):
                start_pos = start_pos + 1
        elif key == curses.KEY_UP:
            if start_pos > 0:
                start_pos = start_pos - 1


def menuCurses(scr_, items_ : list[str])->int:
    """
    menu function

    :param: __curses.window:
    :param: list[str]:
    :return: int:
    """
    curses.curs_set(0)  # Hide cursor
    selected : int = 0
    items_len : int = len(items_)
    height : int
    width : int
    height, width = scr_.getmaxyx()
    height = height - 1

    while True:
        scr_.clear()
        for index, item in enumerate(items_):
            text : str = deepcopy(item)
            if len(text) > width - 3:
                text = text[:(width - 3)]
            if index > height:
                break
            if index == selected:
                scr_.addstr(
                    index,
                    0,
                    f"> {text}",
                    curses.A_REVERSE
                )
            else:
                scr_.addstr(index, 0, f"  {text}")

        scr_.refresh()
        key = scr_.getch()
        if key == curses.KEY_UP:
            selected = (selected - 1) % items_len
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % items_len
        elif key in (curses.KEY_ENTER, 10, 13):
            return selected
        elif key == ord("q"):
            return None
