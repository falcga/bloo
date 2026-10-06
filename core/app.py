import curses
from .loader import load_plugins
from .panel import registry


class Canvas:
    def __init__(self, win, y, x, h, w):
        self.win = win
        self.y, self.x = y, x
        self.h, self.w = h, w

    def addstr(self, dy, dx, text, attr=0):
        if not (0 <= dy < self.h and 0 <= dx < self.w):
            return
        text = str(text)[: self.w - dx]
        try:
            self.win.addstr(self.y + dy, self.x + dx, text, attr)
        except curses.error:
            pass

    def line(self, dy, text="", attr=0):
        self.addstr(dy, 0, " " * self.w)
        self.addstr(dy, 0, text, attr)


class App:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.panels = {}       # "QUOTES" -> cls
        self.current = None    # экземпляр Panel
        self.command_buf = ""
        self.status = ""
        self.running = True

    def run(self):
        curses.wrapper(self._main)

    def switch(self, command):
        cls = self.panels.get(command.upper())
        if cls is None:
            self.status = f"Неизвестная команда: {command}"
            return
        if self.current:
            self.current.deactivate()
        self.current = cls(self)
        self.current.activate()
        self.status = self.current.help or ""
        self.command_buf = ""

    def _main(self, stdscr):
        curses.curs_set(1)
        try:
            curses.start_color()
            curses.use_default_colors()
            for i, c in enumerate((curses.COLOR_CYAN, curses.COLOR_YELLOW,
                                   curses.COLOR_GREEN, curses.COLOR_RED), 1):
                curses.init_pair(i, c, -1)
        except Exception:
            pass
        stdscr.timeout(150)
        stdscr.keypad(True)

        load_plugins(self.plugin_dir)
        for cls in registry():
            if cls.command:
                self.panels[cls.command.upper()] = cls

        if "HELP" in self.panels:
            self.switch("HELP")
        elif self.panels:
            self.switch(next(iter(self.panels)))

        while self.running:
            self._draw(stdscr)
            try:
                ch = stdscr.getch()
            except KeyboardInterrupt:
                break
            if ch == -1:
                continue
            self._handle(ch)

    def _handle(self, ch):
        if ch == 3:                       # Ctrl+C — выход
            self.running = False
            return
        if ch in (curses.KEY_BACKSPACE, 127, 8):
            self.command_buf = self.command_buf[:-1]
            return
        if ch == 27:                      # ESC — очистить строку
            self.command_buf = ""
            return
        if ch in (10, 13, curses.KEY_ENTER):
            cmd = self.command_buf.strip()
            if cmd:
                self.switch(cmd)
            return

        if not self.command_buf and self.current and self.current.handle_key(ch):
            return

        if 32 <= ch < 127:
            self.command_buf += chr(ch)

    def _draw(self, stdscr):
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        title = " MINI-BBG "
        panel_name = self.current.name if self.current else "—"
        header = f"{title}| {panel_name} "
        stdscr.addstr(0, 0, header.ljust(w)[: w - 1], curses.A_REVERSE)

        canvas = Canvas(stdscr, 1, 0, h - 3, w)
        if self.current:
            try:
                self.current.render(canvas)
            except Exception as e:
                canvas.line(0, f"[ошибка панели] {e!r}", curses.A_BOLD)

        stdscr.addstr(h - 2, 0, (self.status or "").ljust(w)[: w - 1], curses.A_DIM)

        prompt = "> " + self.command_buf
        stdscr.addstr(h - 1, 0, prompt.ljust(w - 1)[: w - 1])
        try:
            stdscr.move(h - 1, min(len(prompt), w - 2))
        except curses.error:
            pass
        stdscr.refresh()
