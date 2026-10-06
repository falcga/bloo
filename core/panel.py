"""Базовый класс панели и глобальный реестр.

Любой наследник Panel (кроме помеченных abstract=True) автоматически
попадает в реестр в момент объявления класса — никакого ручного
регистрационного кода плагину писать не нужно.
"""
import curses

_PANELS = []


def registry():
    return list(_PANELS)


def _register(cls):
    if cls not in _PANELS:
        _PANELS.append(cls)


class Panel:
    command = ""       # то что пользователь набирает в командной строке
    name = "Unnamed"   # отображаемое имя
    help = ""          # строка подсказки в статусбаре

    def __init_subclass__(cls, abstract=False, **kwargs):
        super().__init_subclass__(**kwargs)
        if not abstract:
            _register(cls)

    def __init__(self, app):
        self.app = app

    def activate(self):
        """Вызывается при входе на панель."""

    def deactivate(self):
        """Вызывается при уходе с панели."""

    # --- рендер и ввод ---
    def render(self, canvas):
        """Рисует содержимое панели в переданный Canvas."""
        canvas.line(0, self.name, curses.A_BOLD)
        canvas.line(1, "Переопределите render(canvas).")

    def handle_key(self, key):
        """Обработать клавишу, когда командная строка пуста.
        Верните True, чтобы «съесть» клавишу (не пускать в командную строку).
        """
        return False
