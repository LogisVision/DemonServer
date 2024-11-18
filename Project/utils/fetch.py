import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Firebase 초기화
cred = credentials.Certificate("./data/logis_vision.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_and_sort_data():
    # commands 컬렉션의 모든 문서 가져오기
    docs = db.collection("commands").stream()
    
    filtered_data = []
    
    for doc in docs:
        data = doc.to_dict()

        # 중첩 필드에서 robot과 state 조건 체크
        if data.get("robot") == "B" and data.get("state") == "request":
            # destination의 datetime을 파싱하여 저장
            #destination_datetime = data.get("datetime")
            #if destination_datetime:
                # datetime 형식으로 변환
                #destination_datetime = datetime.strptime(destination_datetime, "%Y-%m-%dT%H:%M:%S")
            filtered_data.append(data)
    
    # destination의 datetime을 기준으로 정렬
    filtered_data.sort(key=lambda x: x["datetime"])
    
    return filtered_data


# 함수 실행 예시
sorted_data = fetch_and_sort_data()
for item in sorted_data:
    print(item)
