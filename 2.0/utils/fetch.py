import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime


# Firebase 초기화
cred = credentials.Certificate("./data/logis_vision.json")
firebase_admin.initialize_app(cred)

# 변수 설정 >> 실제 main 함수에서는 var.py에서 설정
robot_type = "A"
is_requested = "completed"

db = firestore.client()

def log_time():
    current_time = datetime.now().strftime("[%Y|%m|%d %H:%M:%S]")
    return current_time

def print_data(data):
    if "destination" in data:
        print("Destination:")
        for key, value in data["destination"].items():
            print(f"  {key.capitalize()}: {value}")

    if "state" in data:
        print("State:")
        print(f"  {data['state']}")

    if "robot" in data:
        print("Robot:")
        print(f"  {data['robot']}")

    if "item" in data:
        print("Item:")
        for key, value in data["item"].items():
            print(f"  {key.capitalize()}: {value}")

def extract_keys(data, keys):
    return {key: data[key] for key in keys if key in data}

def validate_document(data, robot_type, is_requested):
    '''
    단일 데이터 검증 함수
    '''
    required_keys = ["robot", "state", "datetime"]

    # 모든 필요한 키가 존재하는지 확인
    if not all(key in data for key in required_keys):
        print("Skipping invalid documnet: Missing required keys")
        return None

    if data.get("robot") != robot_type or data.get("state") != is_requested:
#        print(data["robot"])
#        print(robot_type)
#        print(data["state"])
#        print(is_requested)
#        print("Skipping document: Does not match robot or state condition")
        return None

#    try:
#        data["datetime"] = datetime.strptime(data["datetime"], "%Y-%m-%dT%H:%M:%S")
#    except ValueError:
#        print("Skipping document: Invalid datetime format")
#        return None

    return data

def fetch_and_sort_data(robot_type, is_requested):
    try:
        # commands 컬렉션의 모든 문서 가져오기
        docs = db.collection("commands").stream()
        
        filtered_data = []
        
        # for문을 돌면서 유효한 데이터셋만 추출
        for doc in docs:
            data = doc.to_dict()
            validated_data = validate_document(data, robot_type, is_requested)
            if validated_data:
                filtered_data.append(validated_data)

        if not filtered_data:
            print("No valid data found matchign thre criteria.")
            return []
        
        # commands의 datetime을 기준으로 정렬
        filtered_data.sort(key=lambda x: x["datetime"])

        keys_to_extract = ["destination", "state", "robot", "item"]
        extracted_data = extract_keys(data, keys_to_extract)

        print_data(extracted_data)

        return extracted_data
        
    # 오류 발생 시
    except Exception as e:
        print(f"Error fetching data from Firebase: {e}")
        return []


# 함수 실행 예시
#sorted_data = fetch_and_sort_data()
#print(sorted_data)
