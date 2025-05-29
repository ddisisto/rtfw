# tmux Clean Config Preview

## Status Bar Example:

```
 RTFW  ◆ PREFIX         0:nexus  •  1:gov  •  2:critic !  •  3:era-1        MOUSE  16:32:15
      ^                    ^          ^         ^                              ^       ^
      └─ Prefix active     │          │         └─ Bell alert (!)             │       └─ Time
                           │          └─ Normal window                         └─ Mouse on
                           └─ Active window (highlighted background)
```

## Key Changes:

1. **Ctrl+Space prefix** - More natural than ~ for frequent use
2. **Clean dots** as separators - Simple `•` instead of ╱ ╲
3. **Background contrast** - Active window has subtle background highlight
4. **Help toggle** - Press `Ctrl+?` to toggle help overlay on/off
5. **Layout moved** - Now `Ctrl+L` since prefix took Ctrl+Space

## Visual Style:
- Active window: Background highlight (#16213e) with bright text
- Normal windows: No background, dimmer text
- Separators: Subtle dots in dark gray
- Alerts: Simple `!` for bells, `*` for activity

## Help Overlay (Ctrl+?):
```
                      RTFW tmux Quick Reference                       
                                                                      
 Navigation: C-Tab/←→         Panes: M-hjkl         Zoom: C-z        
                                                                      
 Splits: C-\\ (vert) C-- (horiz)     Layout: C-l      Mouse: C-m     
                                                                      
 Prefix (C-Space): c=new  x=kill  d=detach  q=numbers  t=clock      
                                                                      
                     Press C-? again to toggle                        
```

The help stays visible until you press Ctrl+? again - no more quick flashing!