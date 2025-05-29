# tmux Styled Config Preview

## What it looks like:

```
◗ RTFW │                  ╱ 0:nexus ╲  ╱ 1:gov ╲  ╱ 2:critic ● ╲                  │ MOUSE  %H:%M:%S ◖
         ^                    ^           ^            ^                              ^        ^
         └─ Session name      │           │            └─ Bell indicator (red ●)      │        └─ Time
                              │           └─ Current window (bold, cyan)              └─ Mouse indicator
                              └─ Normal window (dim)
```

## Key Features:

1. **Clean slate** - All default bindings cleared, only essentials remain
2. **~ prefix** - Single tap to activate, double tap for literal ~
3. **Centered window list** - Symmetric design with ╱ ╲ separators
4. **Cyberpunk aesthetic**:
   - Dark blue/purple base (#1a1a2e, #16213e)
   - Cyan accents (#00d9ff, #7692ff)
   - Red alerts (#e94560)
   - Subtle separators (#53565a)

5. **Unicode indicators**:
   - ◗ ◖ - Session brackets
   - ◆ - PREFIX active
   - ● - Bell alert
   - ◈ - Zoomed pane
   - ╱ ╲ - Window separators

6. **Minimal help** - Only shows what you actually use (press ~?)

## Testing:
```bash
tmux -f tmux-styled.conf new-session -s style-test
```

## Color Palette:
- Background: `#1a1a2e` (deep blue-black)
- Borders: `#2d2d3d` (very dark gray)
- Inactive text: `#a0a0b0` (light gray)
- Active elements: `#00d9ff` (bright cyan)
- Accents: `#7692ff` (soft blue)
- Alerts: `#e94560` (soft red)
- Separators: `#53565a` (dark gray)