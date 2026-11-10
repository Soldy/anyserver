"""
Simplified curses menu
"""
import curses
from copy import deepcopy

def lineToShow(
  text_: str,
  max_: int
) -> list[str]:
    """
    Split the text to lines

    :param: str
    :param: int
    :return: list[str]
    """
    if max_ < 4:
        return['']
    result : list[str] = []
    def newLine(line_:str):
        if line_ != '':
            result.append(str(line_).strip().center(max_))
        return ''
    for line in text_.splitlines():
        words : list[str] = line.split()
        current : str = ''

        for word in words:
            word = word.strip()
            candidate = current
            if len(word) > max_:
                word = word[:max_ - 3] + "..."
                current = newLine(current)
                newLine(word)
                continue
            if candidate != '':
                candidate += ' '
            candidate += word
            if len(candidate) >= max_:
                result.append(current)
                current = word
            else:
                current = candidate
        newLine(current)

    return result

def tableMake(
  rows_ : list[str|dict[str,str|int|float]]|dict[str,dict[str,str|int|float]]
)->str:
    """
    Convert a list of dictionaries into a formatted text table.

    :param: list[str|dict[str,str|int|float]]|dict[str,dict[str,str|int|float]]
    :return: str
    """

    if not rows_ or not rows_[0]:
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
    This is usually managed as admin menus.
    If the item_ comes empty, it is a bug somewhere before this function.
    So we want to crash as soon as possible.
    If we manage the empty items list, it will cause a crash later.
    Debugging becomes more complex.
    So some code are lame.
    How the dope says: Die Motherf*cker

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
                    ("> "+text),
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

def timeMessage(scr_, msg_ : str )->None:
    """
    menu function

    :param: __curses.window:
    :param: str:
    """
    height : int
    width : int
    height, width = scr_.getmaxyx()
    scr_.clear()
    scr_.addstr(
      max((int(height/2)-1), 0),
      max(int((width - len(msg_))/2), 0),
      msg_
    )
    scr_.refresh()
