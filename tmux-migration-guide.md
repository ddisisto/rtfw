# tmux Config Migration Guide

## Testing the New Config

1. **Test in a new session first:**
   ```bash
   tmux -f tmux-enhanced.conf new-session -s test
   ```

2. **Check if Ctrl+Tab works:**
   - Try `Ctrl+Tab` and `Ctrl+Shift+Tab`
   - If captured by terminal, use Settings → Window Manager → Keyboard
   - Look for "Switch to next/previous tab" and remove those bindings

## Key Highlights

### No-Prefix Operations (instant access):
- **Windows**: `Ctrl+Tab/Shift+Tab` or `Ctrl+←→`
- **Panes**: `Alt+hjkl` or `Alt+Arrows`
- **Splits**: `Ctrl+\` (vertical) and `Ctrl+-` (horizontal)
- **Zoom**: `Ctrl+z` (toggle)
- **Layouts**: `Ctrl+Space` (cycle)
- **Mouse**: `Ctrl+m` (toggle on/off)

### Visual Improvements:
- Active pane has green border
- Status shows PREFIX when active
- Status shows MOUSE when enabled
- Window indicators: `!` for bell, `*` for activity, `Z` for zoomed

### Quick Reference:
Press `Prefix+?` to see the cheat sheet anytime!

## Making it Permanent

When happy with the config:
```bash
cp tmux-enhanced.conf tmux.conf
```

## Troubleshooting

**If Ctrl+Tab doesn't work:**
- The fallback `Ctrl+Left/Right` still works
- Check terminal keyboard shortcuts
- Consider `Alt+Tab` as alternative (add these lines):
  ```
  bind-key -n M-Tab next-window
  bind-key -n M-S-Tab previous-window
  ```

**If splits feel backwards:**
- Current: `Ctrl+\` for vertical (side-by-side)
- Current: `Ctrl+-` for horizontal (stacked)
- Swap them in the config if preferred

**Mouse scroll in vim/less:**
- Should work automatically with mouse mode on
- Toggle with `Ctrl+m` if interfering