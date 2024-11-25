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
        self.openai_api_key = "testkey"
        self.client = OpenAI(api_key=self.openai_api_key)

        '''
    def summarize_logs(self, log_data, model="gpt-4", max_tokens=300):
        prompt = f"""
        Here is the log data:

        {log_data}

        Summarize the log contents briefly and count the log levels.
        Provide the result in JSON format string.
        """
        response = self.client.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
        '''

    def summarize_logs(self, log_data, model="gpt-4o", max_tokens=150, temperature=0.5):
        prompt = f"""
    Here is the log data:

    {log_data}

    1. Determine the time range (start and end time) of the logs.
    2. Summarize the logs really briefly.
    3. Count the occurrences of each log level (critical, error, warning, info, total).
    4. Provide the result in JSON format string, like this:

       {{
           "datetime_range": {{
               "start": "YYYY-mm-DD HH-MM-SS",  # Example: 2024-11-25
               "end": "YYYY-mm-DD HH-MM-SS"
           }},
           "description": "breif summary here",
           "log_counts": {{
               "critical": X,
               "error": X,
               "info": X,
               "total": X,
               "warning": X,
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
'''

    def read_log_file(file_path, duration=60):
        """
        Read log file and retrieve a specific number of lines.
        :param file_path: Path to the log file.
        :param duration: Number of lines to retrieve.
        :return: Log data as a string.
        """
        try:
            with open(file_path, 'r') as file:
                logs = file.readlines()
                log_data = ''.join(logs[:duration])
                return log_data
        except Exception as e:
            Logger().error(f"Error reading log file: {e}")
            return None
'''
