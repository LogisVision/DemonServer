import firebase_admin
from firebase_admin import credentials, db
import time

# Firebase 서비스 계정 키 파일 경로
cred = credentials.Certificate('./data/firebase_key.json')  # 서비스 계정 키 파일 경로 입력

# Firebase 앱 초기화
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://agvproject-1f9ae-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# 데이터 변경을 감지할 함수 정의
def print_changed_data(old_data, new_data):
    """이전 데이터와 현재 데이터를 비교하여 변경된 부분을 출력"""
    for key in new_data:
        if key not in old_data:
            print(f"새로운 항목 추가: {key} = {new_data[key]}")
        elif old_data[key] != new_data[key]:
            print(f"변경된 항목: {key} = {new_data[key]} (이전 값: {old_data[key]})")
    
    # 삭제된 항목 확인
    for key in old_data:
        if key not in new_data:
            print(f"삭제된 항목: {key}")

# Firebase 실시간 데이터베이스에서 'test' 경로에 대한 리스너 추가
ref = db.reference('/')

# 간단한 폴링으로 데이터가 변경되었는지 감지하는 코드
last_data = ref.get()
while True:
    current_data = ref.get()
    if current_data != last_data:
        print_changed_data(last_data or {}, current_data or {})  # 변경된 데이터만 출력
        last_data = current_data  # 최신 데이터로 업데이트
    time.sleep(1)  # 1초 간격으로 체크

