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

import serial_meth

def make_layout():
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
    )
    layout["body"].split_row(
        Layout(name="side", minimum_size=13),
        Layout(name="main", ratio=10, minimum_size=10),
    )
    layout["main"].split(
        Layout(name="term", ratio=10, minimum_size=10),
        Layout(name="input", minimum_size = 3)
    )
    return layout

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
    terminal.add_column(style="white", no_wrap=True)
    terminal.add_column(style="white", no_wrap=True)

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

def readSerial(serialPort, layout, terminal, serial_lines, curr_index, end_index):
    line = serial_meth.readSerialLine(serialPort)

    if line != None:
        length = len(line)
        if length > 0:
            serial_lines.append(line)
            end_index += 1

            refillTable(layout, terminal, serial_lines, curr_index, end_index)

        return end_index 
    else:
        return None

def disconnectKeyInputs():
    if msvcrt.kbhit():
        key = ord(msvcrt.getch())

        if key == 27: #ESC
                return None
        elif key == 32: #Space
                return 1
        else:
            return 0
    
    return 0

def checkKeyInputs(serialPort, layout, terminal, serial_lines, curr_index, end_index, line):
    if msvcrt.kbhit():
        key = ord(msvcrt.getch())

        if key == 27: #ESC
                return None, 0, 0
        elif key == 8: #Backspace
            if len(line) > 0:
                line = line[:-1]
                layout["input"].update(
                    Panel(
                        "[bold]Enter Text:[/bold] [white]" + line + "[/white]",
                        border_style="medium_purple"
                    )
                )
        elif key == 13: #Enter
            #end_index += 1
            #serial_lines.append(line)
            serial_meth.writeSerialLine(serialPort, line)
            line = ''
            layout["input"].update(
                Panel(
                    "[bold]Enter Text:[/bold] ",
                    border_style="medium_purple"
                )
            )
            
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

            layout["input"].update(
                Panel(
                    "[bold]Enter Text:[/bold] [white]" + line + "[/white]",
                    border_style="medium_purple"
                )
            )
    
    return line, curr_index, end_index