import logging
from config import config


class CaseRunLog(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(CaseRunLog, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = self.init_logger()

    def log(self, message, level):
        if config.log_enable:
            if level == logging.ERROR:
                self.logger.error(message)
            if level == logging.CRITICAL:
                self.logger.critical(message)
            if level == logging.WARNING:
                self.logger.warning(message)
            if level == logging.INFO:
                self.logger.info(message)
            if level == logging.FATAL:
                self.logger.fatal(message)
            if level == logging.DEBUG:
                self.logger.debug(message)

    @classmethod
    def init_logger(cls):
        logger = logging.getLogger('autoTest')
        logger.setLevel(config.log_level)
        log_file_handle = logging.FileHandler(config.running_log_path, 'w' if config.only_save_last else 'a', encoding='utf8')
        log_file_handle.setLevel(config.log_level)
        formatter = logging.Formatter(config.log_format)
        log_file_handle.setFormatter(formatter)
        logger.addHandler(log_file_handle)
        return logger
