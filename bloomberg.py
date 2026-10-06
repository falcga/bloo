"""Мини-Bloomberg. Запуск: python bloomberg.py"""
import os
import sys
from core.app import App


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    App(plugin_dir=os.path.join(here, "plugins")).run()


if __name__ == "__main__":
    main()
