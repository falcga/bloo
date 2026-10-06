import curses
from core.panel import Panel


class KeypadPanel(Panel):
    command = "KEYS"
    name = "Keypad"
    help = "Стрелки двигают маркер. Ввод текста по-прежнему идёт в командную строку."

    def activate(self):
        self.x, self.y = 20, 4
        self.log = []

    def render(self, canvas):
        canvas.line(0, "Нажимайте стрелки.", curses.A_BOLD)
        cy = max(2, min(self.y, canvas.h - 5))
        cx = max(0, min(self.x, canvas.w - 2))
        canvas.addstr(cy, cx, "◆", curses.color_pair(2) | curses.A_BOLD)
        for i, msg in enumerate(self.log[-3:]):
            canvas.line(canvas.h - 4 + i, msg, curses.A_DIM)

    def handle_key(self, key):
        moves = {
            curses.KEY_UP: (0, -1), curses.KEY_DOWN: (0, 1),
            curses.KEY_LEFT: (-1, 0), curses.KEY_RIGHT: (1, 0),
        }
        if key in moves:
            dx, dy = moves[key]
            self.x = max(0, self.x + dx * 2)
            self.y = max(2, self.y + dy)
            self.log.append(f"move dx={dx:+d} dy={dy:+d}  ->  x={self.x} y={self.y}")
            return True
        return False
