## IMPORTS ##
import serial.tools.list_ports
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
from collections import namedtuple
import msvcrt
import enum
 
SerialConfig = namedtuple("SerialConfig", "port baudrate bytesize timeout stopbits")

class alerts(enum.Enum):
    success = 0
    noPorts = 1
    leave = 2

port = None
baudrate = 115200
bytesize = 8
timeout = 2
stopbits = serial.STOPBITS_ONE
    
def make_layout():
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
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

def displaySelections(layout, table, title, items, choice):
    table = Table.grid()
    table.add_column("Choose Port", justify="center")
    table.add_row("[b light_steel_blue1][underline]" + title + "[/underline][/b light_steel_blue1]")

    for index, item in enumerate(items):
        if choice == index:
            table.add_row("[b blue]" + item + "[/b blue]")
        else: 
            table.add_row(item)

    layout["body"].update(
        Panel(
            Align.center(
                Align.center(table),
                vertical="middle",
            ),
            box=box.ROUNDED,
            padding=(2, 2),
            title="",
            border_style="white",
        )
    )

def selections(layout, table, title, items):
    done = False
    choice = 0
    end = len(items)

    displaySelections(layout, table, title, items, choice)
    
    while not done:
        time.sleep(0.01)

        if msvcrt.kbhit():
            key = ord(msvcrt.getch())

            if key == 13: #Enter
                done = True
                
            elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
                key = ord(msvcrt.getch())

                if key == 80: #Down arrow
                    choice = (choice - 1) % end

                elif key == 72: #Up arrow
                    choice = (choice + 1) % end
                
                displaySelections(layout, table, title, items, choice)
        
    return items[choice]
            
def getPorts(layout, port_table):
    layout["body"].update(Panel("There are many ports"))
    #ports = serial.tools.list_ports.comports()
    ports = ["COM3", "COM2"]
    # User chooses COM port
    if len(ports) == 1: # If there is only 1, choose it
        layout["body"].update(Panel("Openning " + ports[0] + "..."))
        return ports[0]
    elif len(ports) > 1: # User chooses port
        layout["body"].update(Panel("There are many ports"))
        return selections(layout, port_table, "Select Port...", ports)
    else: # There are no ports
        layout["body"].update(Panel("No COM ports open."))
        return alerts.noPorts

def openSerial(layout, port, baudrate, bytesize, timeout, stopbits):
    try:
        serialPort = serial.Serial(
            port = port,
            baudrate=baudrate,
            bytesize=bytesize, 
            timeout=timeout, 
            stopbits=stopbits
        )
        return serialPort
    
    except:
        layout["body"].update(Panel("Unable to open serial port"))
        return None

def reattempt(layout, message):
    reattempt_table = Table.grid()
    reattempt_table.add_column(justify="center")
    return True if selections(layout, reattempt_table, message, ["yes", "nes"]) == "yes" else False

def start():
    port_table = Table.grid()
    port_table.add_column(justify="center")
    port_table.add_row("[b light_steel_blue1][underline]Choose a Port[/underline][/b light_steel_blue1]")
    
    layout = make_layout()
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

    done = False
    
    with Live(layout, refresh_per_second=10, screen=True) as live:
        while not done:
            port = getPorts(layout, port_table)

            if port == alerts.noPorts:
                if not reattempt(layout, "There are not Ports open... Try again?"):
                    return -1
            elif port == alerts.leave:
                if reattempt(layout, "Select 'Yes' to exit program..."):
                    return -1
            else:
                done = True

        layout["body"].update(Panel(str(port) + " chosen"))
        time.sleep(2)

        serial_connect = openSerial(layout, port, 115200, 8, 2, serial.STOPBITS_ONE)

        while not serial_connect:
            if not reattempt(layout, "Cannot connect to " + port + ". \nWould you like to try again?"):
                    return -1
        
        return 0
