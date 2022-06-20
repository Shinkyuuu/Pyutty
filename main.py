import serial
import serial.tools.list_ports
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
import loading

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
                    return None, None
            elif port == setup_disp.alerts.leave:
                if setup_disp.reattempt(layout, "Select 'Yes' to exit program..."):
                    return None, None
            else:
                done = True

        layout["body"].update(Panel(str(port) + " chosen"))
        sleep(2)

        serialPort = setup_disp.openSerial(
            layout, 
            port, 
            115200, 
            8, 
            2, 
            serial.STOPBITS_ONE
        )

        while not serialPort:
            if not setup_disp.reattempt(layout, "Cannot connect to " + str(port) + ". \nWould you like to try again?"):
                    return None, None
        
        return SerialConfig(port.device, 115200, 8, 2, serial.STOPBITS_ONE), serialPort

def main_start(serialConfig, serialPort):
    terminal = Table.grid()
    terminal.add_column(style="white", no_wrap=False)
    terminal.add_column(style="white", no_wrap=False)

    layout = main_disp.make_layout()
    layout["header"].update(Header())
    layout["side"].update(main_disp.make_settings(
        str(serialConfig.port),
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
    counter = 0
    cnt_ref = 1
    serial_lines = []
    curr_index = 0
    end_index = len(serial_lines) - 1
    line = ""

    with Live(layout, refresh_per_second=10, screen=True) as live:
        while not done:
            sleep(.02)
            
            status = main_disp.readSerial(serialPort, layout, terminal, serial_lines, curr_index, end_index)

            if status == None:
                serialPort.close()
                layout["input"].update(
                    Panel(
                        Align.center(
                            Align.center("[bold][white]Connection Lost... (Press |esc| to continue): [/white][/bold]"),
                            vertical="middle",
                        ),
                        border_style="medium_purple"
                    )
                )

                status = main_disp.disconnectKeyInputs()
                while status == 0:
                    status = main_disp.disconnectKeyInputs()

                if status == None:
                    done = True
            else:
                end_index = status
            
            line, curr_index, end_index = main_disp.checkKeyInputs(serialPort, layout, terminal, serial_lines, curr_index, end_index, line)
            if line == None:
                done = True
            # else:
            #     end_index = status
                
            #     line, curr_index, end_index = main_disp.checkKeyInputs(serialPort, layout, terminal, serial_lines, curr_index, end_index, line)
            #     if line == None:
            #         done = True

    return None
            
def loading_start():
    load = Progress()
    load.add_task("[red]Loading", 5)

    layout = loading.make_layout()
    layout["header"].update(Header())    
    layout["body"].update(
        Panel(
            Align.center(
                Align.center(load),
                vertical="middle",
            ),
            title="",
            border_style="light_steel_blue1",
            padding=(2, 2),
        )
    )

    with Live(layout, refresh_per_second=10, screen=True):
        while not load.finished:
            sleep(0.1)
            for i in range(28):
                load.advance(load.tasks[0].id)


done = False

while not done:
    serialConfig, serialPort = setup_start()

    if serialConfig and serialPort:
        loading_start()
        ans = main_start(serialConfig, serialPort)
        serialPort.close()
        loading_start()
    else:
        done = True
