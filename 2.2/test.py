from utils.chatgpt_logger_analyzer import ChatGPTLoggerAnalyzer 
from utils.firebase_handler import FirebaseHandler 

openai_api_key = "sample_api"
firebase_cred_path = "./data/logis_vision.json"
log_file_path = "./app.log"

duration_minutes = 5  # 최근 5분의 로그를 분석
collection_name = "log_analysis"
document_name = "latest_summary"

credential_path = "./data/logis_vision.json"
collection_name = "commands"

firebase_handler = FirebaseHandler(credential_path, collection_name)
'''
# ChatGPTLoggerAnalyzer 인스턴스 생성
analyzer = ChatGPTLoggerAnalyzer(openai_api_key, firebase_cred_path)

# 로그 분석 및 결과 출력
result = analyzer.process_log_file(
    log_file_path,
    duration_minutes,
    collection_name,
    document_name
)

print("Analysis result updated in Firebase:")
print(result)
'''

firebase_handler.to_progress("AYqxwvUtu2IAzqBaRU1z")
