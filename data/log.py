# log.py
import logging
import sys


class ColoredFormatter(logging.Formatter):
    """Форматтер с цветным выводом"""

    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',  # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'  # Reset
    }

    def format(self, record):
        original = super().format(record)
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        return f"{color}{original}{self.COLORS['RESET']}"


# Глобальная настройка логгера
def setup_logger():
    logger = logging.getLogger('pyrogram_bot')
    logger.setLevel(logging.DEBUG)

    # Очищаем старые обработчики
    if logger.handlers:
        logger.handlers.clear()

    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredFormatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))

    # Файловый обработчик
    file_handler = logging.FileHandler('data/bot.log', 'w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Создаем глобальный логгер
logger = setup_logger()