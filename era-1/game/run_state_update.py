#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from engine.state_engine import StateEngine

engine = StateEngine(
    Path(__file__).parent.parent.parent,  # project root
    Path(__file__).parent.parent.parent / "_sessions"
)

print("Updating all agent states...")
engine.poll_cycle()
print("Done! Check agent/_state.md files")