import requests
import json
import time

# Firebase Realtime Database의 데이터 URL
url = "https://agvproject-1f9ae-default-rtdb.asia-southeast1.firebasedatabase.app/"

def listen_to_firebase(url):
    while True:  # 무한 루프로 재연결 시도
        try:
            print("Firebase에 연결 중...")
            response = requests.get(url, stream=True)  # 스트림 모드로 연결

            # 연결이 끊어지기 전까지 반복
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data: "):  # Firebase 스트림 데이터 포맷
                        data = json.loads(decoded_line[6:])  # "data: " 이후의 JSON 데이터만 추출
                        print("데이터 변경 감지:", data)
                        
        except requests.exceptions.RequestException as e:
            print("연결 오류 발생:", e)
            print("5초 후 재연결 시도 중...")
            time.sleep(5)  # 5초 후 재연결 시도

# 실시간 스트리밍 시작
listen_to_firebase(url)

