import sys
import logging
import argparse
from PyQt5.QtWidgets import QApplication

from src.objects.snakegame import SnakeGame

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="log level handler")
    parser.add_argument("--loglevel",
                        default="WARNING",
                        help="Niveau de log (ex: DEBUG, INFO, WARNING)")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.loglevel.upper(), logging.WARNING))

    app = QApplication(sys.argv)
    snake_game = SnakeGame()
    sys.exit(app.exec_())
