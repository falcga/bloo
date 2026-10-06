import curses
from core.panel import Panel


class HelpPanel(Panel):
    command = "HELP"
    name = "Help"
    help = "Список панелей. Введите команду и нажмите Enter. Ctrl+C — выход."

    def render(self, canvas):
        canvas.line(0, "Доступные панели:", curses.A_BOLD)
        canvas.line(1, "─" * min(canvas.w - 1, 60))
        for i, (cmd, cls) in enumerate(sorted(self.app.panels.items()), start=2):
            if i >= canvas.h - 1:
                break
            canvas.addstr(i, 2, cmd.ljust(10),
                          curses.color_pair(1) | curses.A_BOLD)
            canvas.addstr(i, 13, cls.name.ljust(20))
            canvas.addstr(i, 34, cls.help or "")
