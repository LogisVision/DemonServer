from utils.chatgpt_logger_analyzer import LogAnalyzer 
from utils.firebase_handler import FirebaseHandler 
from datetime import datetime
import time
import re
import json

# ChatGPTLoggerAnalyzer 인스턴스 생성
credential_path = "./data/logis_vision.json"
collection_name = "logs"

# 로그 분석 및 결과 출력
log_analyzer = LogAnalyzer()
firebase_handler = FirebaseHandler(credential_path, collection_name)


log_path = "./app.log"
log_data = log_analyzer.read_log_file(log_path)


response_content = log_analyzer.summarize_logs(log_data)

log_data = log_analyzer.save_response_to_json(response_content)

'''
print(date)
struct_time = time.strptime(date ,"%Y-%m-%d %H:%M:%S")
timestamp = time.mktime(struct_time)
print(timestamp)
'''

firebase_handler.upload_logs_with_timestamps(log_data, "logs")
