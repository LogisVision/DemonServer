import builtins
from datetime import datetime

class Logger:
    @staticmethod
    def log_time():
        """현재 시간 기록용 함수"""
        return datetime.now().strftime("[%Y|%m|%d %H:%M:%S]")

    @staticmethod
    def print_with_time(*args, **kwargs):
        """시간 로깅을 포함한 print 함수"""
        time_prefix = Logger.log_time()
        builtins.print(time_prefix, *args, **kwargs)  # 기존 print 함수 호출
