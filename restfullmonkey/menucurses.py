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
    scr_.clear()
    lines = str(text_).splitlines()
# wip code part
# pylint: disable=C0200
# pylint: disable=W0612
    height, width = scr_.getmaxyx()
    for i in range(len(lines)):
        scr_.addnstr(i, 0, lines[i], width - 1)
# pylint: enable=C0200
# pylint: enable=W0612
    scr_.refresh()
    scr_.getch()

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
