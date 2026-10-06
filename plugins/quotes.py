import curses
import random
import time
from core.panel import Panel

_TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "BRK.B"]


class QuotesPanel(Panel):
    command = "QUOTES"
    name = "Quotes"
    help = "Псевдо-котировки. Обновляются автоматически раз в секунду."

    def activate(self):
        self.prices = {t: random.uniform(50, 500) for t in _TICKERS}
        self.deltas = {t: 0.0 for t in _TICKERS}
        self.last = time.time()

    def render(self, canvas):
        now = time.time()
        if now - self.last > 1:
            for t in _TICKERS:
                d = random.uniform(-1.5, 1.5)
                self.prices[t] = max(1.0, self.prices[t] + d)
                self.deltas[t] = d
            self.last = now

        canvas.line(0, "  Тикер      Цена        Δ", curses.A_BOLD)
        canvas.line(1, "─" * min(canvas.w - 1, 40))
        for i, t in enumerate(_TICKERS, start=2):
            d = self.deltas[t]
            color = curses.color_pair(3) if d >= 0 else curses.color_pair(4)
            canvas.addstr(i, 2, t.ljust(10), curses.A_BOLD)
            canvas.addstr(i, 12, f"{self.prices[t]:>10.2f}")
            canvas.addstr(i, 24, f"{d:+6.2f}", color)
        canvas.line(canvas.h - 1, "Цены синтетические",
                    curses.A_DIM)
