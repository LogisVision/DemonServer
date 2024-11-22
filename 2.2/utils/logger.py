import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_file="app.log", log_level=logging.DEBUG):
        """
        Logger 클래스 초기화
        :param log_file: 로그 파일 경로
        :param log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger("app_logger")
        self.logger.setLevel(log_level)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self._setup_handlers(log_file)
    def _setup_handlers(self, log_file):
        """
        핸들러 설정: 파일 핸들러와 콘솔 핸들러 추가
        """
        # 포매터 설정
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 파일 핸들러 (로테이팅)
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)

        # 핸들러 추가
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
