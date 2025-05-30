#!/usr/bin/env python3
"""
Test the v2 state models - structure matches template
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from engine.models_v2 import AgentGroundState, GitActivity, ContextWindow, LastObservedAgentState, AgentState
from engine.state_parser_v2 import StateParserV2


def test_serialization():
    """Test that model structure matches template exactly"""
    print("Testing State Model v2")
    print("=" * 60)
    
    # Create a test state
    state = AgentGroundState(
        agent_name="test",
        git_activity=GitActivity(
            last_read_commit_hash="abc123def456",
            last_read_commit_timestamp=datetime.now(),
            last_write_commit_hash="789012345678",
            last_write_commit_timestamp=datetime.now()
        ),
        context_window=ContextWindow(
            session_id="test-session-123",
            context_tokens=50000,
            context_percent=39.1,
            last_updated=datetime.now()
        ),
        last_observed_agent_state=LastObservedAgentState(
            state=AgentState.DIRECT_IO,
            thread="test-thread",
            started=datetime.now(),
            expected_next_state="inbox",
            unread_message_count=5
        )
    )
    
    # Serialize
    content = state.to_state_file_content()
    print("\nGenerated _state.md:")
    print("-" * 60)
    print(content)
    
    # Parse it back
    parser = StateParserV2()
    parsed = parser.parse_content(content)
    
    print("\nParsed back:")
    print("-" * 60)
    print(f"Format version: {parsed.format_version}")
    print(f"Git activity: {parsed.git_activity}")
    print(f"Context window: {parsed.context_window}")
    print(f"Agent state: {parsed.last_observed_agent_state}")
    
    # Test with real file
    print("\n\nTesting with real _state.md files:")
    print("-" * 60)
    
    project_root = Path(__file__).parent.parent.parent
    for agent in ["era-1", "critic", "gov", "nexus"]:
        state_file = project_root / agent / "_state.md"
        if state_file.exists():
            parsed = parser.parse_file(state_file)
            print(f"\n{agent.upper()}:")
            print(f"  State: {parsed.last_observed_agent_state.state.value}")
            print(f"  Context: {parsed.context_window.context_percent}%")
            print(f"  Unread: {parsed.last_observed_agent_state.unread_message_count}")


if __name__ == "__main__":
    test_serialization()