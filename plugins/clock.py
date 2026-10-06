import curses
import time
from core.panel import Panel


class ClockPanel(Panel):
    command = "CLOCK"
    name = "Clock"
    help = "Текущее время и дата."

    def render(self, canvas):
        now = time.localtime()
        hhmmss = time.strftime("%H:%M:%S", now)
        date = time.strftime("%A, %d %B %Y", now)
        canvas.line(2, hhmmss.center(canvas.w),
                    curses.A_BOLD | curses.color_pair(1))
        canvas.line(4, date.center(canvas.w))
