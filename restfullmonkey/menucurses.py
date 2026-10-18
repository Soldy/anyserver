"""
Simplified curses menu
"""


import curses
import copy

def tableMake(rows):
    """
    Convert a list of dictionaries into a formatted text table.
    """

    if not rows:
        return ""
    # fix the path dict to list
    if isinstance(rows, dict):
        columns = []
        row_checked = []
        for i in rows:
            newrow = {}
            newrow['name'] = str(i)
            for a in rows[i]:
                newrow[a] = str(rows[i][a])
            row_checked.append(copy.deepcopy(newrow))
        rows = row_checked
    # Use dictionary keys as column nameso
    columns = list(rows[0].keys())


    # Calculate width for each column
    widths = {}

    for column in columns:
        values = [str(row.get(column, "")) for row in rows]
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

    table.extend(format_row(row) for row in rows)
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
            scr_.addnstr(i, 0, lines[i+start_pos], width - 1)
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

def menuCurses(scr_, items)->int:
    """
    menu function

    :param: __curses.window:
    :param: list[str]:
    :return: int:
    """
    curses.curs_set(0)  # Hide cursor
    selected = 0

    while True:
        scr_.clear()

        for index, item in enumerate(items):
            if index == selected:
                scr_.addstr(
                    index,
                    0,
                    f"> {item}",
                    curses.A_REVERSE
                )
            else:
                scr_.addstr(index, 0, f"  {item}")

        scr_.refresh()

        key = scr_.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(items)

        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(items)

        elif key in (curses.KEY_ENTER, 10, 13):
            return selected

        elif key == ord("q"):
            return None
