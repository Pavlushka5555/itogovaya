import logging


def setup_logger(log_file='error.log'):
    """Настройка логгера"""
    # Создание объекта логгера
    slogger = logging.getLogger('error_logger')
    slogger.setLevel(logging.ERROR)  # Установка уровня логгирования на ERROR

    # Создание обработчика для записи логов в файл
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.ERROR)  # Установка уровня логгирования на ERROR

    # Создание форматировщика для логов
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру, если его нет
    if not slogger.handlers:
        slogger.addHandler(file_handler)

    return slogger


# Инициализация логгера
logger = setup_logger()


# Функция для логирования ошибок
def log_error(error_msg):
    """Логирование ошибки"""
    logger.error(error_msg)