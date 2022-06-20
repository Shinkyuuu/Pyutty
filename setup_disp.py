## IMPORTS ##
import serial as serial
from serial.tools import list_ports
import sys
import os
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

def displaySelections(layout, table, items, choice):
    table = Table.grid()
    table.add_column(justify="center")

    for index, item in enumerate(items):
        if choice == index:
            table.add_row("[b blue]" + item + "[/b blue]")
        else: 
            table.add_row(item)

    layout["body"].update(
        Panel(
            table,
            box=box.ROUNDED,
            padding=(2, 2),
            title="",
            border_style="white",
        )
    )

def selections(layout, table, items):
    done = False
    choice = 0
    end = len(items)

    displaySelections(layout, table, items, choice)
    
    while not done:
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            
            if key == 27: #ESC
                    choice = -1
                    done = True
            elif key == 13: #Enter
                done = True
                
            elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
                key = ord(msvcrt.getch())

                if key == 75 and 0 <= choice - 1 <= end: #Down arrow
                    choice -= 1

                elif key == 77 and 0 <= curr_index + 1 <= end: #Up arrow
                    choice += 1
                
                displaySelections(layout, table, items, choice)
        
        return choice
            
def getPorts(layout, port_table):
    ports = list_ports.comports()

    # User chooses COM port
    if len(found) == 1: # If there is only 1, choose it
        layout["body"].update(Panel("Openning " + ports[0] + "..."))
        return ports[0]
    elif len(found) > 1: # User chooses port
        return selections(layout, port_table, ports)
    else: # There are no ports
        layout["body"].update(Panel("No COM ports open."))
        return -1

def getPorts():
    ports = serial.tools.list_ports.comports()
    found = dict()

    # Find and list all COM ports
    for i, p in enumerate(ports):
        found[i] = p.device
        print(f"{i}: {p.device}")
    
    # User chooses COM port
    if len(found) == 1: # If there is only 1, choose it
        print(f"Chose {found[0]}")
        return found[0]
    elif len(found) > 1: # User chooses port
        chosen = found[int(input("Chose COM Port (0, 1, ...): "))]
        print(f"Chose {chosen}")
        return chosen
    else: # There are no ports
        print("No COM Ports Open")
    
    return None

def getSerialLine():
    try:
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):

            # Print the contents of the serial data
            return str(serialPort.readline().decode('Ascii'), end = '')
    # If connection is lost or user types (ctrl + c)
    except:
        serialPort.close()
        return None

def openSerial(layout, port, baudrate, bytesize, timeout, stopbits):
    try:
        serialPort = serial.Serial(
            port = port,
            baudrate=baudrate,
            bytesize=bytesize, 
            timeout=timeout, 
            stopbits=stopbits
        )
    
    except:
        layout["body"].update(Panel("Unable to open serial port"))

def start():
    port_table = Table.grid()
    port_table.add_column(justify="center")
    
    layout = make_layout()
    layout["header"].update(Header())
    layout["body"].update(
        Panel(
            port_table,
            box=box.ROUNDED,
            padding=(2, 2),
            title="",
            border_style="white",
        )
    )

    port = getPorts(layout, port_table)
    openSerial(layout, port, 115200, 8, 2, serial.STOPBITS_ONE)
    