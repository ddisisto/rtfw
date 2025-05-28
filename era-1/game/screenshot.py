#!/home/daniel/prj/rtfw/era-1/game/.venv/bin/python3
"""
Foundation Terminal - Screenshot Mode
Renders a static view of the terminal for documentation/demos
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich.style import Style

# Define phosphor amber colors
AMBER = "#FFAA00"
AMBER_DIM = "#AA7700"
AMBER_DARK = "#664400"
ALERT = "#FF6600"


def create_screenshot():
    """Create a static screenshot of the Foundation Terminal"""
    console = Console()
    
    # Create main layout
    layout = Layout()
    
    # Header
    header_text = Text("Foundation Terminal v0.1.0", style=f"bold {AMBER}")
    header_text.append("                  ", style="")
    header_text.append(datetime.now().strftime("%H:%M:%S"), style=f"dim {AMBER}")
    header = Panel(Align.center(header_text), style=f"{AMBER} on black")
    
    # Agent list
    agent_table = Table(show_header=False, show_edge=False, box=None, padding=0)
    agent_table.add_column("Agent", style=AMBER)
    agent_table.add_row("@ERA-1    [deep_work]", style=f"bold {AMBER}")
    agent_table.add_row("@GOV      [     idle]", style=AMBER_DIM)  
    agent_table.add_row("@NEXUS    [    inbox]", style=AMBER)
    agent_table.add_row("@CRITIC   [  distill]", style=ALERT)  # High context
    
    agents_panel = Panel(
        agent_table,
        title="═ AGENTS ═",
        title_align="center",
        style=AMBER_DIM,
        border_style=AMBER_DIM
    )
    
    # Commands
    commands = """[S]tatus - All agents
[M]essage - Send commit
[T]okens - Context usage
[L]og - System activity
[D]istill - Force distill
[I]nject - State change
[R]efresh - Update now
[H]elp - Show help
[Q]uit - Exit terminal"""
    
    commands_panel = Panel(
        commands,
        title="═ COMMANDS ═",
        title_align="center",
        style=AMBER_DIM,
        border_style=AMBER_DIM
    )
    
    # Agent details
    details_text = f"""State: deep_work
Thread: tui-implementation
Context: 17.0% (21760/128000)
Session: cc9298f1-253c-4abf-aa62-51bf8c1bf8b1
Last Commit: 0e77103 (2m ago)
Unread: 0"""
    
    details_panel = Panel(
        details_text,
        title="═ @ERA-1 ═",
        title_align="center",
        style=AMBER,
        border_style=AMBER_DIM
    )
    
    # Activity log
    activity_text = """00:15:39 State transition: inbox → deep_work
00:14:22 Commit: Updated state engine v2
00:13:15 Context warning: 80% threshold
00:12:01 Message from @GOV: state protocols ready
00:10:45 Distillation complete"""
    
    activity_panel = Panel(
        activity_text,
        title="═ ACTIVITY LOG ═",
        title_align="center",
        style=AMBER_DIM,
        border_style=AMBER_DIM
    )
    
    # Footer
    footer_text = "[Q] Quit  [R] Refresh  [M] Message  [S] Status  [H] Help"
    footer = Panel(footer_text, style=AMBER_DIM)
    
    # Combine layout
    layout.split_column(
        Layout(header, size=3),
        Layout(name="main"),
        Layout(footer, size=3)
    )
    
    layout["main"].split_row(
        Layout(name="sidebar", size=20),
        Layout(name="content")
    )
    
    layout["sidebar"].split_column(
        Layout(agents_panel, size=15),
        Layout(commands_panel)
    )
    
    layout["content"].split_column(
        Layout(details_panel, size=8),
        Layout(activity_panel)
    )
    
    # Print the layout
    console.print(layout)


if __name__ == "__main__":
    create_screenshot()