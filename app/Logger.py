import logging


def get_logger() -> logging.getLogger():
    """Возвращает настроенный логгер
        """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Обработчик для записи данных в файл
    logger_handler = logging.FileHandler('app_logs.log')
    logger_handler.setLevel(logging.INFO)

    # Formatter для форматирования сообщений в логе
    logger_formatter = logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s')

    # Formatter добавляется в обработчик
    logger_handler.setFormatter(logger_formatter)

    # Добавление обработчика в Logger
    logger.addHandler(logger_handler)

    return logger
