import serial
import time
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
from collections import namedtuple
import setup_disp
import main_disp


SerialConfig = namedtuple("SerialConfig", "port baudrate bytesize timeout stopbits")

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

#status = setup_disp.start()
def setup_start():
    port_table = Table.grid()
    port_table.add_column(justify="center")
    port_table.add_row("[b light_steel_blue1][underline]Choose a Port[/underline][/b light_steel_blue1]")
    
    layout = setup_disp.make_layout()
    layout["header"].update(Header())
    layout["body"].update(
        Panel(
            Align.center(
                Align.center(port_table),
                vertical="middle",
            ),
            box=box.ROUNDED,
            padding=(2, 2),
            title="",
            border_style="white",
        )
    )

    with Live(layout, refresh_per_second=10, screen=True) as live:
        done = False

        while not done:
            port = setup_disp.getPorts(layout, port_table)

            if port == setup_disp.alerts.noPorts:
                if not setup_disp.reattempt(layout, "There are not Ports open... Try again?"):
                    return None
            elif port == setup_disp.alerts.leave:
                if setup_disp.reattempt(layout, "Select 'Yes' to exit program..."):
                    return None
            else:
                done = True

        layout["body"].update(Panel(str(port) + " chosen"))
        time.sleep(2)

        serial_connect = setup_disp.openSerial(
            layout, 
            port, 
            115200, 
            8, 
            2, 
            serial.STOPBITS_ONE
        )

        while not serial_connect:
            if not setup_disp.reattempt(layout, "Cannot connect to " + port + ". \nWould you like to try again?"):
                    return SerialConfig(port, 115200, 8, 2, serial.STOPBITS_ONE)
        
        return SerialConfig(port, 115200, 8, 2, serial.STOPBITS_ONE)

def main_start(serialConfig):
    terminal = Table.grid()
    terminal.add_column(style="white", no_wrap=False)
    terminal.add_column(style="white", no_wrap=False)

    layout = main_disp.make_layout()
    layout["header"].update(Header())
    layout["side"].update(main_disp.make_settings(
        serialConfig.port,
        str(serialConfig.baudrate),
        str(serialConfig.bytesize),
        str(serialConfig.timeout),
        str(serialConfig.stopbits)
    ))
    layout["term"].update(
        Panel(
            terminal,
            box=box.ROUNDED,
            padding=(1, 2),
            title="Serial Terminal",
            border_style="white",
        )
    )
    layout["input"].update(
        Panel(
            "[bold]Enter Text:[/bold] ",
            border_style="medium_purple"
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
                    end_index += 1
                    serial_lines.append(line)
                    line = ''
                    layout["input"].update(
                        Panel(
                            "[bold]Enter Text:[/bold] ",
                            border_style="medium_purple"
                        )
                    )

                    main_disp.refillTable(layout, terminal, serial_lines, curr_index, end_index)
                    
                elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
                    key = ord(msvcrt.getch())

                    if key == 80 and 0 <= curr_index + 1 <= end_index: #Down arrow
                        curr_index += 1

                    elif key == 72 and 0 <= curr_index - 1 <= end_index: #Up arrow
                        curr_index -= 1
                    
                    main_disp.refillTable(layout, terminal, serial_lines, curr_index, end_index)

                else:
                    line += chr(key)

                    layout["input"].update(
                        Panel(
                            "[bold]Enter Text:[/bold] [white]" + line + "[/white]",
                            border_style="medium_purple"
                        )
                    )

serialConfig = setup_start()

if serialConfig:
    main_start(serialConfig)
