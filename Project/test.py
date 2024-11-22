from utils.chatgpt_logger_analyzer import LogAnalyzer 
import re
import json

# ChatGPTLoggerAnalyzer 인스턴스 생성


# 로그 분석 및 결과 출력
log_analyzer = LogAnalyzer()


log_path = "./app.log"
log_data = log_analyzer.read_log_file(log_path)


response_content = log_analyzer.summarize_logs(log_data)

log_analyzer.save_response_to_json(response_content)

#save_responsse_to_json(summary

