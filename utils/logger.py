import logging
import sys
from logging.handlers import RotatingFileHandler

class LoggerService:
    def __init__(self, log_file="logs/app.log", level=logging.INFO):
        self.logger = logging.getLogger("ChatBotLogger")
        self.logger.setLevel(level)

        # Формат логов
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

        # Обработчик для файла с ротацией
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)

        # Обработчик для вывода в консоль
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)

        # Добавляем обработчики в логгер
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
