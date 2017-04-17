import logging

# Воспользуемся модулем logging для удобства отслеживания работы с мьютексом и без него
# Этот модуль является потоко-безопасным, поэтому при работе с потоками
# лучше использовать его для фиксирования событий
def get_logger(name, filename):
    logger = logging.getLogger(name)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
    fh = logging.FileHandler(filename, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)
    return logger