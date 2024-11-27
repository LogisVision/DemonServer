import json
from datetime import datetime, timezone
from openai import OpenAI
from decouple import config
from .logger import Logger
import pytz


class LogAnalyzer:
    def __init__(self):
        """
        Initialize the LogAnalyzer with OpenAI API key.
        """
        self.openai_api_key = "sample key"
        self.client = OpenAI(api_key=self.openai_api_key)

    def summarize_logs(self, log_data, model="gpt-4o", max_tokens=150, temperature=0.5):
        prompt = f"""
        다음은 로그 데이터입니다:

        {log_data}

        1. 로그의 시간 범위(시작 시간과 종료 시간)를 결정하세요.
        2. 로그를 간략하게 요약하세요.
        3. 각 로그 레벨(critical, error, warning, info, total)의 발생 횟수를 세세요.
        4. 결과를 JSON 형식 문자열로 제공하세요. 예시는 다음과 같습니다:

        {{
            "datetime_range": {{
                "start": "YYYY-mm-DD HH-MM-SS",  # 예: 2024-11-25
                "end": "YYYY-mm-DD HH-MM-SS"
            }},
            "description": "여기에 간략한 요약을 작성",
            "log_counts": {{
                "critical": X,
                "error": X,
                "info": X,
                "total": X,
                "warning": X
            }}
        }}
        """
        response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                    ],
                model=model,
                max_tokens=max_tokens,
                temperature=temperature
                )
        return response.choices[0].message.content

    @staticmethod
    def save_response_to_json(response_content):
        """
        Save OpenAI API response to a JSON file.
        :param response_content: Response content from OpenAI API.
        :param file_path: Path to save the JSON file.
        """
        # parsing the string
        cleaned_string = response_content[7:-3]
        try:
            # JSON 문자열을 파이썬 딕셔너리로 변환
            response_dict = json.loads(cleaned_string.strip())
            print(response_dict)
            return response_dict
        except json.JSONDecodeError as e:
            Logger().error(f"JSONDecodeError 발생: {e} ")

            '''
        try:
            response_json = json.loads(response_content)
            with open(file_path, "w") as file:
                json.dump(response_json, file, indent=4)
            print(f"Response saved to JSON file: {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error parsing response content as JSON: {e}")
            '''
    @staticmethod

    def read_log_file(file_path, start_time=None, end_time=None):
        """
        Read log file and retrieve lines within a specific time range.

        :param file_path: Path to the log file.
        :param start_time: Start of the time range (datetime object).
        :param end_time: End of the time range (datetime object).
        :return: Filtered log data as a string.
        """
        local_tz = pytz.timezone('Asia/Seoul')
        try:
            with open(file_path, 'r') as file:
                logs = file.readlines()
                filtered_logs = []

                print(start_time)
                print(end_time)
                for line in reversed(logs):
                    try:
                        log_time_str = line.split(']')[0].strip('[')  # [2024-11-25 14:43:13] -> 2024-11-25 14:43:13
                        log_time = local_tz.localize(datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S"))

                        #log_time = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=local_tz)
                    
                        if (start_time is None or log_time >= start_time) and (end_time is None or log_time <= end_time):
                            print(line)
                            filtered_logs.append(line)
                    except (ValueError, IndexError):
                        continue

                return ''.join(filtered_logs)
        except Exception as e:
            Logger().error(f"Error reading log file: {e}")
            return None
