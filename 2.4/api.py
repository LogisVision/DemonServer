import os
from decouple import config
from openai import OpenAI
import json

# 환경 변수에서 API 키 로드
api_key = config('OPENAI_API_KEY')

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

# 로그 데이터 요약 생성 함수
def summarize_logs(log_data, model="gpt-4o", max_tokens=150, temperature=0.5):
    prompt = f"""
    Here is the log data:

    {log_data}

    1. Determine the time range (start and end time) of the logs.
    2. Summarize the logs briefly.
    3. Count the occurrences of each log level (critical, error, warning, info, total).
    4. Provide the result in JSON format, like this:
       {{
           "time_range": {{
               "start_time": "YYYY-MM-DD HH:MM:SS",
               "end_time": "YYYY-MM-DD HH:MM:SS"
           }},
           "summary": "Log summary here",
           "log_levels": {{
               "critical": X,
               "error": X,
               "info": X,
               "warning": X,
               "total": X
           }}
       }}
    """
    response = client.chat.completions.create(
        messages=[
            {"role": "system", 
             "content": 
             "You are a helpful assistant."},
            {"role": "user",
             "content": prompt}
        ],
        model=model,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response

# 로그 파일 읽기 (1분 분량)
def read_log_file(file_path, duration=60):
    try:
        with open(file_path, 'r') as file:
            logs = file.readlines()
            # 여기에서 duration에 맞게 데이터를 선택 (간단한 예: 상위 60줄 선택)
            log_data = ''.join(logs[:duration])
        return log_data
    except Exception as e:
        print(f"Error reading log file: {e}")
        return None

# JSON 파일로 저장하는 함수
def save_response_to_json(response_content, file_path):
    try:
        # JSON 데이터 파싱
        response_json = json.loads(response_content)

        # JSON 파일로 저장
        with open(file_path, "w") as file:
            json.dump(response_json, file, indent=4)

        print(f"Response saved to JSON file: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error parsing response content as JSON: {e}")

# 로그 파일 경로 설정
log_file_path = "./app.log"

# 로그 데이터 가져오기
log_data = read_log_file(log_file_path)

if log_data:
    # 로그 데이터 요약 요청
    dialogue = summarize_logs(log_data)

    # 결과 출력
    summary = dialogue.choices[0].message.content.strip()
    print("Summary of the logs:")
    print(summary)

    # JSON 파일로 저장
    save_response_to_json(summary, "./log_analysis.json")

    # 사용된 토큰 수 출력
    total_tokens = dialogue.usage.total_tokens
    print(f"Total tokens used: {total_tokens}")
else:
    print("No log data to process.")
