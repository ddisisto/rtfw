#!/usr/bin/env python3
"""
Lifecycle Command Implementations

Implements STATE, TOKENS, THREADS commands per agent-lifecycle protocol.
These commands provide visibility into the living system.
"""

from typing import Dict, Any, List
from core_interfaces import CommandHandler, Command, AgentState
import json
from datetime import datetime, timezone

class StateCommand(CommandHandler):
    """
    STATE command - Show all agent states with lifecycle info
    
    Displays:
    - Current lifecycle state (inbox/deep_work/idle/etc)
    - Active thread if in deep_work
    - Time in current state
    - Visual state indicators
    """
    
    def can_handle(self, command: Command) -> bool:
        return command.name.upper() == "STATE"
    
    def execute(self, command: Command, context: Dict[str, Any]) -> Dict[str, Any]:
        state_provider = context['state']
        agents = state_provider.get_all_agents()
        
        if command.args:
            # Specific agent requested
            agent_name = command.args[0].lower()
            agent = next((a for a in agents if a.name.lower() == agent_name), None)
            if agent:
                return {'output': self._format_single_agent(agent)}
            else:
                return {'error': f'Unknown agent: {agent_name}'}
        
        # All agents
        return {'output': self._format_all_agents(agents)}
    
    def _format_all_agents(self, agents: List) -> str:
        """Format state display for all agents"""
        lines = [
            "SYSTEM STATE MONITOR",
            "=" * 70,
            ""
        ]
        
        # Header
        lines.append(f"{'AGENT':<10} {'STATE':<12} {'THREAD':<20} {'TIME':<10} {'STATUS'}")
        lines.append("-" * 70)
        
        for agent in agents:
            state_str = self._format_state(agent.state)
            thread_str = agent.thread[:18] + ".." if agent.thread and len(agent.thread) > 20 else (agent.thread or "-")
            time_str = self._format_time_in_state(agent)
            status_str = self._get_status_indicator(agent)
            
            lines.append(
                f"{agent.name:<10} {state_str:<12} {thread_str:<20} {time_str:<10} {status_str}"
            )
        
        # Summary
        lines.append("")
        lines.append("SUMMARY:")
        working = sum(1 for a in agents if a.state == AgentState.DEEP_WORK)
        idle = sum(1 for a in agents if a.state == AgentState.IDLE)
        active = sum(1 for a in agents if a.is_active)
        
        lines.append(f"  Active: {active}/{len(agents)} | Working: {working} | Idle: {idle}")
        
        return "\n".join(lines)
    
    def _format_single_agent(self, agent) -> str:
        """Detailed state for single agent"""
        lines = [
            f"AGENT: {agent.name}",
            f"STATE: {self._format_state(agent.state)}",
            f"THREAD: {agent.thread or 'none'}",
            f"TIME IN STATE: {self._format_time_in_state(agent)}",
            "",
            "CONTEXT WINDOW:",
            f"  Tokens: {agent.context_tokens:,} ({agent.context_percent}%)",
            f"  Status: {self._get_context_status(agent.context_percent)}",
            "",
            "ACTIVITY:",
            f"  Last Write: {agent.last_write_commit[:7]} ({self._format_age(agent.last_write_time)})",
            f"  Last Read: {agent.last_read_commit[:7]} ({self._format_age(agent.last_read_time)})",
            f"  Unread Messages: {agent.unread_messages}",
        ]
        
        if agent.state == AgentState.IDLE:
            lines.append("\nIDLE REASON: Waiting for dependencies")  # Would come from state
            
        return "\n".join(lines)
    
    def _format_state(self, state: AgentState) -> str:
        """Format state with color codes for terminal"""
        state_colors = {
            AgentState.DEEP_WORK: "\033[32m",  # Green
            AgentState.IDLE: "\033[33m",       # Yellow
            AgentState.DISTILL: "\033[36m",    # Cyan
            AgentState.INBOX: "\033[34m",      # Blue
            AgentState.LOGOUT: "\033[31m",     # Red
            AgentState.DIRECT_IO: "\033[35m",  # Magenta
        }
        color = state_colors.get(state, "")
        reset = "\033[0m" if color else ""
        return f"{color}{state.value}{reset}"
    
    def _format_time_in_state(self, agent) -> str:
        """Format time since state transition"""
        # This would come from tracking state transitions
        # For now, approximate from last activity
        ref_time = agent.last_write_time
        now = datetime.now(timezone.utc)
        
        if ref_time.tzinfo is None:
            ref_time = ref_time.replace(tzinfo=timezone.utc)
            
        delta = now - ref_time
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        
        if delta.days > 0:
            return f"{delta.days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def _format_age(self, dt: datetime) -> str:
        """Format datetime as age"""
        now = datetime.now(timezone.utc)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        delta = now - dt
        if delta.days > 0:
            return f"{delta.days}d ago"
        
        hours = delta.seconds // 3600
        if hours > 0:
            return f"{hours}h ago"
            
        minutes = delta.seconds // 60
        return f"{minutes}m ago"
    
    def _get_status_indicator(self, agent) -> str:
        """Get visual status indicator"""
        if agent.context_percent > 90:
            return "🔴 CRITICAL"
        elif agent.context_percent > 85:
            return "🟡 HIGH"
        elif agent.unread_messages > 15:
            return "📬 MESSAGES"
        elif agent.state == AgentState.IDLE:
            return "💤 WAITING"
        elif agent.state == AgentState.DEEP_WORK:
            return "🔨 WORKING"
        else:
            return "✓ OK"
    
    def _get_context_status(self, percent: float) -> str:
        """Get context status description"""
        if percent < 60:
            return "🟢 Healthy"
        elif percent < 85:
            return "🟡 Elevated"
        elif percent < 95:
            return "🟠 High - consider distill"
        else:
            return "🔴 Critical - logout imminent"


class TokensCommand(CommandHandler):
    """
    TOKENS command - Context window usage visualization
    
    Shows:
    - Current token usage per agent
    - Visual meter representation
    - Growth rate estimates
    - Time until forced logout
    """
    
    def can_handle(self, command: Command) -> bool:
        return command.name.upper() == "TOKENS"
    
    def execute(self, command: Command, context: Dict[str, Any]) -> Dict[str, Any]:
        state_provider = context['state']
        agents = state_provider.get_all_agents()
        
        lines = [
            "CONTEXT WINDOW MONITOR",
            "=" * 70,
            ""
        ]
        
        # Header
        lines.append(f"{'AGENT':<10} {'TOKENS':<12} {'PERCENT':<8} {'METER':<20} {'EST. TIME'}")
        lines.append("-" * 70)
        
        for agent in agents:
            meter = self._create_meter(agent.context_percent)
            est_time = self._estimate_time_remaining(agent)
            
            lines.append(
                f"{agent.name:<10} {agent.context_tokens:>10,}  {agent.context_percent:>5.1f}%  {meter:<20} {est_time}"
            )
        
        # System totals
        total_tokens = sum(a.context_tokens for a in agents)
        lines.append("")
        lines.append(f"SYSTEM TOTAL: {total_tokens:,} tokens")
        
        # Legend
        lines.append("")
        lines.append("LEGEND: [🟩] 0-60% | [🟨] 60-85% | [🟥] 85-100%")
        
        return {'output': '\n'.join(lines)}
    
    def _create_meter(self, percent: float) -> str:
        """Create visual meter for token usage"""
        width = 20
        filled = int(width * percent / 100)
        
        if percent < 60:
            char = "🟩"
        elif percent < 85:
            char = "🟨"
        else:
            char = "🟥"
        
        meter = char * filled + "⬜" * (width - filled)
        return f"[{meter}]"
    
    def _estimate_time_remaining(self, agent) -> str:
        """Estimate time until forced logout based on growth rate"""
        if agent.context_percent >= 95:
            return "LOGOUT NOW"
        elif agent.context_percent >= 90:
            return "< 30 min"
        elif agent.state != AgentState.DEEP_WORK:
            return "-"
        
        # Estimate based on NEXUS observations: 5-10K tokens/hour normal
        remaining_percent = 90 - agent.context_percent
        remaining_tokens = int(remaining_percent * 1500)  # Assume 150K window
        
        # Conservative estimate: 10K/hour
        hours = remaining_tokens / 10000
        
        if hours < 1:
            return f"~{int(hours * 60)}m"
        else:
            return f"~{hours:.1f}h"


class ThreadsCommand(CommandHandler):
    """
    THREADS command - Active work threads across system
    
    Shows:
    - All active threads
    - Which agent owns each thread
    - Thread duration
    - Related commits
    """
    
    def can_handle(self, command: Command) -> bool:
        return command.name.upper() == "THREADS"
    
    def execute(self, command: Command, context: Dict[str, Any]) -> Dict[str, Any]:
        state_provider = context['state']
        agents = state_provider.get_all_agents()
        
        # Collect active threads
        threads = []
        for agent in agents:
            if agent.thread and agent.state in [AgentState.DEEP_WORK, AgentState.DISTILL]:
                threads.append({
                    'agent': agent.name,
                    'thread': agent.thread,
                    'state': agent.state,
                    'start_time': agent.last_write_time,  # Approximation
                })
        
        if not threads:
            return {'output': "No active threads. All agents idle or in inbox processing."}
        
        lines = [
            "ACTIVE THREADS",
            "=" * 70,
            ""
        ]
        
        for t in threads:
            duration = self._format_duration(t['start_time'])
            state = "working" if t['state'] == AgentState.DEEP_WORK else "distilling"
            
            lines.append(f"Thread: {t['thread']}")
            lines.append(f"  Agent: {t['agent']} ({state})")
            lines.append(f"  Duration: {duration}")
            lines.append("")
        
        lines.append(f"Total active threads: {len(threads)}")
        
        return {'output': '\n'.join(lines)}
    
    def _format_duration(self, start_time: datetime) -> str:
        """Format thread duration"""
        now = datetime.now(timezone.utc)
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
            
        delta = now - start_time
        
        if delta.days > 0:
            return f"{delta.days}d {delta.seconds // 3600}h"
        
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"


class InjectCommand(CommandHandler):
    """
    INJECT command - Add message to agent inbox
    Admin-only command for async communication
    """
    
    def can_handle(self, command: Command) -> bool:
        return command.name.upper() == "INJECT"
    
    def execute(self, command: Command, context: Dict[str, Any]) -> Dict[str, Any]:
        if len(command.args) < 2:
            return {'error': 'Usage: INJECT @AGENT "message"'}
        
        agent_name = command.args[0].lstrip('@')
        message = ' '.join(command.args[1:])
        
        message_provider = context['messages']
        
        # Add timestamp and source
        full_message = f"[ADMIN INJECT {datetime.now().isoformat()}] {message}"
        
        try:
            message_provider.inject_to_inbox(agent_name, full_message)
            return {'output': f"Message injected to @{agent_name}'s inbox"}
        except Exception as e:
            return {'error': f"Failed to inject message: {str(e)}"}


"""
These commands provide real-time visibility into the agent lifecycle.
The game becomes a window into the living system, showing:

1. What each agent is doing (STATE)
2. How much context they're using (TOKENS)
3. What work is in progress (THREADS)
4. Ability to communicate async (INJECT)

ERA-2 can enhance these with graphical representations,
but the core data and logic remains here.
"""