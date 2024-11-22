# utils/chatgpt_logger_analyzer.py
import openai
import re
import json
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

class ChatGPTLoggerAnalyzer:
    def __init__(self, openai_api_key, firebase_cred_path):
        """
        ChatGPTLoggerAnalyzer 초기화
        :param openai_api_key: OpenAI API 키
        :param firebase_cred_path: Firebase 인증서 경로
        """
        openai.api_key = openai_api_key
        self.db = self._initialize_firebase(firebase_cred_path)

    @staticmethod
    def _initialize_firebase(cred_path):
        """
        Firebase 초기화
        """
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        return firestore.client()

    def read_log_file(self, log_file_path, duration_minutes=5):
        """
        로그 파일에서 특정 시간 범위의 로그를 읽어옴
        :param log_file_path: 로그 파일 경로
        :param duration_minutes: 분석할 시간 범위 (분)
        :return: 시간 필터링된 로그 문자열
        """
        now = datetime.now()
        start_time = now - timedelta(minutes=duration_minutes)
        filtered_logs = []

        with open(log_file_path, 'r') as file:
            for line in file:
                match = re.match(r'\[(.*?)\]', line)
                if match:
                    log_time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                    if start_time <= log_time <= now:
                        filtered_logs.append(line)

        return '\n'.join(filtered_logs)

    def analyze_logs(self, logs):
        """
        ChatGPT API를 사용해 로그를 분석 및 요약
        :param logs: 로그 문자열
        :return: 요약 결과
        """
        prompt = f"""You are an expert log analyzer. Analyze the following logs and provide:
1. A summary of the logs.
2. The number of each log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
Logs:
{logs}
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert log analyzer."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        return response['choices'][0]['message']['content']

    def calculate_log_levels(self, logs):
        """
        로그 레벨별 개수 계산
        :param logs: 로그 문자열
        :return: 로그 레벨별 개수 (딕셔너리)
        """
        levels = ['INFO', 'WARNING', 'ERROR', 'CRITICAL']
        level_counts = {level: 0 for level in levels}

        for line in logs.splitlines():
            for level in levels:
                if f"[{level}]" in line:
                    level_counts[level] += 1

        return level_counts

    def update_firebase(self, collection_name, document_name, data):
        """
        Firebase에 분석 결과 업데이트
        :param collection_name: 컬렉션 이름
        :param document_name: 문서 이름
        :param data: 업데이트할 데이터 (딕셔너리)
        """
        doc_ref = self.db.collection(collection_name).document(document_name)
        doc_ref.set(data)

    def process_log_file(self, log_file_path, duration_minutes, collection_name, document_name):
        """
        전체 로그 처리 파이프라인
        :param log_file_path: 로그 파일 경로
        :param duration_minutes: 분석할 시간 범위 (분)
        :param collection_name: Firebase 컬렉션 이름
        :param document_name: Firebase 문서 이름
        """
        logs = self.read_log_file(log_file_path, duration_minutes)
        log_levels = self.calculate_log_levels(logs)
        summary = self.analyze_logs(logs)

        # 데이터 구성
        result_data = {
            "start_time": logs.splitlines()[0][1:20],
            "end_time": logs.splitlines()[-1][1:20],
            "log_levels": log_levels,
            "summary": summary
        }

        # Firebase에 업데이트
        #self.update_firebase(collection_name, document_name, result_data)
        return result_data
