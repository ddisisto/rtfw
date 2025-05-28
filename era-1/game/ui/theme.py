"""
Foundation Terminal - Phosphor Theme
1982 amber terminal aesthetic
"""

PHOSPHOR_CSS = """
/* Main application styling */
Screen {
    background: #000000;
}

/* Phosphor amber colors */
.active {
    color: #FFAA00;
    text-style: bold;
}

.idle {
    color: #AA7700;
}

.offline {
    color: #664400;
}

.alert {
    color: #FF6600;
    text-style: bold blink;
}

/* Headers and titles */
Header {
    background: #000000;
    color: #FFAA00;
    text-style: bold;
}

Footer {
    background: #000000;
    color: #AA7700;
}

/* Main layout */
#main {
    height: 100%;
}

#sidebar {
    width: 20;
    border-right: heavy #AA7700;
    padding: 0 1;
}

#agent-list {
    height: 60%;
    border: round #AA7700;
    padding: 1;
    margin-bottom: 1;
}

#commands {
    height: 40%;
    border: round #AA7700;
    padding: 1;
}

#agent-details {
    padding: 1;
}

/* Data tables */
DataTable {
    background: #000000;
    color: #FFAA00;
}

DataTable > .datatable--header {
    background: #000000;
    color: #FFAA00;
    text-style: bold;
}

DataTable > .datatable--cursor {
    background: #AA7700;
    color: #000000;
}

DataTable > .datatable--hover {
    background: #332200;
}

/* Text elements */
Static {
    color: #FFAA00;
}

Label {
    color: #AA7700;
}

/* Input fields */
Input {
    background: #000000;
    border: solid #AA7700;
    color: #FFAA00;
}

Input:focus {
    border: solid #FFAA00;
}

/* Buttons */
Button {
    background: #000000;
    border: solid #AA7700;
    color: #AA7700;
}

Button:hover {
    background: #332200;
    color: #FFAA00;
    border: solid #FFAA00;
}

Button:focus {
    background: #AA7700;
    color: #000000;
}

/* Containers */
Container {
    background: #000000;
}

/* Scrollbars */
ScrollBar {
    background: #000000;
}

ScrollBar > .scrollbar--bar {
    color: #664400;
}

ScrollBar > .scrollbar--bar-active {
    color: #AA7700;
}

/* Notifications */
Toast {
    background: #AA7700;
    color: #000000;
    border: double #FFAA00;
}

/* Add subtle scanline effect via gradient (if supported) */
#main {
    background: $background;
}
"""