#!/home/daniel/prj/rtfw/era-1/game/.venv/bin/python3
"""
Foundation Terminal - Entry Point
The game interface that IS the development environment
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ui.app import FoundationTerminal


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        prog="Foundation Terminal",
        description="The game interface that IS the development environment",
        epilog="Part of the rtfw project - riding the fourth wall"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s v0.1.0 (ERA-1)"
    )
    
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug mode with verbose logging"
    )
    
    parser.add_argument(
        "--no-engine",
        action="store_true", 
        help="Run without state engine (UI testing mode)"
    )
    
    
    parser.add_argument(
        "--theme",
        choices=["amber", "green", "white"],
        default="amber",
        help="Terminal phosphor color theme (default: amber)"
    )
    
    parser.add_argument(
        "--oneshot", "--capture", "--screenshot",
        action="store_true",
        help="Capture initial state and exit (no interaction)"
    )
    
    return parser.parse_args()


def main():
    """Launch the Foundation Terminal"""
    args = parse_args()
    
    # Create app with configuration
    app = FoundationTerminal()
    
    # Apply configuration from args
    if args.debug:
        app.debug_mode = True
        
    if args.no_engine:
        app.use_engine = False
        
    app.color_theme = args.theme
    
    # Handle oneshot mode
    if args.oneshot:
        # Import and run screenshot mode instead
        from screenshot import create_screenshot
        create_screenshot()
        return
    
    # Run the app
    app.run()


if __name__ == "__main__":
    main()