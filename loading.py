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
from rich.progress import track

timer = 100

def make_layout():
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
    )

    return layout


    
