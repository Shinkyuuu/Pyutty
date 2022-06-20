from datetime import datetime
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.live import Live
from time import sleep
import msvcrt

def make_layout():
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
    )
    layout["body"].split_row(
        Layout(name="side", minimum_size=13),
        Layout(name="main", ratio=10, minimum_size=30),
    )
    layout["main"].split(
        Layout(name="term", ratio=10, minimum_size=30),
        Layout(name="input", minimum_size = 5)
    )
    return layout

class Header:
    def __rich__(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Pyutty[/b] Serial Terminal",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on medium_purple4")

def make_settings(port, baudrate, bytesize, timeout, stopbits):
    settings = Table.grid(padding=0)
    settings.add_column(style="white", justify="center")
    settings.add_row("[b light_steel_blue1][underline]Port[/underline][/b light_steel_blue1]")
    settings.add_row(port + '\n')
    settings.add_row("[b light_steel_blue1][underline]Baud Rate[/underline][/b light_steel_blue1]")
    settings.add_row(baudrate + '\n')
    settings.add_row("[b light_steel_blue1][underline]Byte Size[/underline][/b light_steel_blue1]")
    settings.add_row(bytesize + '\n')
    settings.add_row("[b light_steel_blue1][underline]Timeout[/underline][/b light_steel_blue1]")
    settings.add_row(timeout + '\n')
    settings.add_row("[b light_steel_blue1][underline]Stop Bits[/underline][/b light_steel_blue1]")
    settings.add_row(stopbits)

    settings_panel = Panel(
        Align.center(settings),
        box=box.ROUNDED,
        title="[bold]Settings[/bold]",
        border_style="light_steel_blue1",
        padding=(2, 1)
    )

    return settings_panel

def refillTable(layout, terminal_table, serial_lines, index, end):
    terminal = Table.grid()
    terminal.add_column(style="white")
    terminal.add_column(style="white")

    for i, line in enumerate(serial_lines[index:]):
        terminal.add_row(str(i + index), "  " + line)

    layout["term"].update(
        Panel(
            terminal,
            box=box.ROUNDED,
            padding=(1, 2),
            title="Serial Terminal",
            border_style="white",
        )
    )

def start():
    terminal = Table.grid()
    terminal.add_column(style="white")
    terminal.add_column(style="white")

    layout = make_layout()
    layout["header"].update(Header())
    layout["side"].update(make_settings())
    layout["term"].update(
        Panel(
            terminal,
            box=box.ROUNDED,
            padding=(1, 2),
            title="Serial Terminal",
            border_style="white",
        )
    )

    done = False
    serial_lines = []
    curr_index = 0
    end_index = len(serial_lines) - 1
    line = ""

    with Live(layout, refresh_per_second=10, screen=True) as live:
        while not done:
            sleep(.01)

            if msvcrt.kbhit():
                key = ord(msvcrt.getch())
                
                if key == 27: #ESC
                        done = True
                elif key == 13: #Enter
                    end_index += 1
                    serial_lines.append(line)
                    line = ''

                    refillTable(layout, terminal, serial_lines, curr_index, end_index)
                    
                elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
                    key = ord(msvcrt.getch())

                    if key == 80 and 0 <= curr_index + 1 <= end_index: #Down arrow
                        curr_index += 1

                    elif key == 72 and 0 <= curr_index - 1 <= end_index: #Up arrow
                        curr_index -= 1
                    
                    refillTable(layout, terminal, serial_lines, curr_index, end_index)

                else:
                    line += chr(key)                    
