import logging
import datetime

from logging.handlers import RotatingFileHandler
from logging import FileHandler, StreamHandler

class Logger:
    def __init__(self, appname, file_level=None, consol_level=None):
        self.appname = appname
        self.file_level = file_level
        self.consol_level = consol_level

    def return_loggit(self):
        logger = logging.getLogger(self.appname)
        handlers = []
        if self.file_level is not None:
            logger.setLevel(getattr(logging, self.file_level.upper()))
            fh = logging.handlers.RotatingFileHandler(
                self.log_file_path,
                maxBytes=10000000,
                backupCount=3)
            fh.setLevel(getattr(logging, self.file_level.upper()))
            fh.setFormatter(self.log_format)
            handlers.append(fh)
            # handlers.append(logging.FileHandler(self.log_file_path))
        if self.consol_level is not None:
            logger.setLevel(getattr(logging, self.consol_level.upper()))
            ch = logging.StreamHandler()
            ch.setLevel(getattr(logging, self.consol_level.upper()))
            ch.setFormatter(self.log_format)
            handlers.append(ch)

        for handler in handlers:
            logger.addHandler(handler)

        return logger

    @property
    def log_file_path(self):
        return f"logs/{self.appname}.log"
    
    @property
    def log_format(self):
        return logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s - %(message)s', '%Y-%m-%dT%H:%M:%SZ')