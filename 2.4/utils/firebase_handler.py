import firebase_admin
import pytz
import time
from firebase_admin import credentials, firestore
from .logger import Logger
from datetime import datetime

class FirebaseHandler:
    def __init__(self, credential_path, collection_name):
        # Firebase 초기화
        if not firebase_admin._apps:
            cred = credentials.Certificate(credential_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.collection_name = collection_name

    @staticmethod
    def print_data(data):
        """데이터 출력"""
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

    @staticmethod
    def extract_keys(data, keys):
        """특정 키만 추출"""
        return {key: data[key] for key in keys if key in data}

    @staticmethod
    def validate_document(data, robot_type, is_requested):
        """
        단일 데이터 검증 함수
        """
        required_keys = ["robot", "state", "datetime"]

        # 모든 필요한 키가 존재하는지 확인
        if not all(key in data for key in required_keys):
            Logger().warning("Skipping invalid document: Missing required keys")
            return None

        if data.get("robot") != robot_type or data.get("state") != is_requested:
            return None

        return data

    def to_process(self, command_id):
        """
        Firebase에서 데이터를 lock된 데이터를 해제
        """
        try:
            # 컬렉션의 모든 문서 가져오기
            docs = self.db.collection(self.collection_name).stream()

            # for문을 돌면서 유효한 데이터셋만 추출
            for doc in docs:
                data = doc.to_dict()
                if doc.id == command_id and data["state"] == "request":
                    doc.reference.update({"state" : "progress", })
                    Logger().info(f"Updated 'state' for document {doc.id} to completed")
        except Exception as e:
            Logger().error(f"Error fetching data from Firebase: {e}")
            return []


    def fetch_and_sort_data(self, robot_type, is_requested):
        """
        Firebase에서 데이터를 가져와 정렬
        """
        try:
            # 컬렉션의 모든 문서 가져오기
            docs = self.db.collection(self.collection_name).stream()
            filtered_data = []

            # for문을 돌면서 유효한 데이터셋만 추출
            for doc in docs:
                data = doc.to_dict()
                # data에 command_id에 해당하는 값 추가
                data["id"] = doc.id
                validated_data = self.validate_document(data, robot_type, is_requested)
                if validated_data:
                    filtered_data.append(validated_data)

            if not filtered_data:
                Logger().warning("No valid data found matching the criteria.")
                return []

            # datetime을 기준으로 정렬
            filtered_data.sort(key=lambda x: x["datetime"])

            # 필요한 키만 추출
            keys_to_extract = ["destination", "state", "robot", "item", "id"]
            extracted_data = [self.extract_keys(data, keys_to_extract) for data in filtered_data]

            # 정렬된 데이터 출력
#            for data in extracted_data:
#                self.print_data(data)

            return extracted_data

        except Exception as e:
            Logger().error(f"Error fetching data from Firebase: {e}")
            return []

    def upload_json_to_firestore(json_file_path, collection_name):
        try:
            # JSON 파일 읽기
            with open(json_file_path, "r") as file:
                data = json.load(file)
            
            # Firestore에 데이터 업로드
            doc_ref = db.collection(collection_name).document()
            doc_ref.set(data)
            
            print(f"Data successfully uploaded to Firestore collection: {collection_name}")
        except Exception as e:
            Logger().error(f"Error uploading data to Firestore: {e}")


    def to_progress(self, command_id):
        """
        Firebase에서 데이터를 lock된 데이터를 해제
        """
        try:
            # 컬렉션의 모든 문서 가져오기
            docs = self.db.collection(self.collection_name).stream()

            # for문을 돌면서 유효한 데이터셋만 추출
            for doc in docs:
                data = doc.to_dict()
                if doc.id == command_id and data["state"] == "request":
                    doc.reference.update({"state" : "progress", })
                    Logger().info(f"Updated 'state' for document {doc.id} to progress")
# status change
            docs = self.db.collection(self.collection_name).stream()
        except Exception as e:
            Logger().error(f"Error changing state from request to progress: {e}")
            return []

    def unlock_data(self, robot_type, command_id):
        """
        Firebase에서 데이터를 lock된 데이터를 해제
        """
        try:
            # 컬렉션의 모든 문서 가져오기
            docs = self.db.collection(self.collection_name).stream()

            # for문을 돌면서 유효한 데이터셋만 추출
            for doc in docs:
                data = doc.to_dict()
                print(data)
                if doc.id == command_id and data["state"] == "progress":
                    doc.reference.update({"state" : "completed", })
                    Logger().info(f"Updated 'state' for document {doc.id} to completed")
                elif 'forward' in data and data["state"] == "lock":
                    forward_path = data["forward"].path.split('/',1)[1]
                    if forward_path == command_id:
                        doc.reference.update({"state" : "request", })
                        Logger().info(f"Updated 'state' for document {doc.id} to request")
        except Exception as e:
            Logger().error(f"Error fetching data from Firebase: {e}")
            return []


    def upload_logs_with_timestamps(self, log_data, collection_name):
        """
        주어진 로그 데이터를 Firestore에 업로드하며, time_range 내 날짜를 Timestamp로 변환.

        Args:
        log_data (dict): Firestore에 업로드할 데이터 딕셔너리.
        collection_name (str): Firestore 컬렉션 이름.
        document_name (str): Firestore 문서 이름.
        """
        try:
                # 날짜 문자열을 datetime으로 변환 후 Timestamp로 변환
            datetime_range = log_data.get('datetime_range', {})
            start_time_str = datetime_range.get('start')
            end_time_str = datetime_range.get('end')

            print(f"start time : {start_time_str}")
            print(f"end time : {end_time_str}")
            # 문자열을 datetime으로 변환 (포맷: "Month-Day-Year")
            local_tz = pytz.timezone('Asia/Seoul')
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=local_tz).astimezone(pytz.utc) if start_time_str else None
            
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=local_tz).astimezone(pytz.utc) if end_time_str else None

            print(start_time)
            print(end_time)
            # Firestore Timestamp로 변환
            if start_time:
                log_data['datetime_range']['start'] = start_time
            if end_time:
                log_data['datetime_range']['end'] = end_time

            # Firestore에 데이터 업로드
            '''
            doc_ref = self.db.collection(collection_name).document(document_name)
            doc_ref.set(log_data)
            '''
            doc_ref = self.db.collection(collection_name).add(log_data)
            print(f"Logs successfully uploaded to Firestore: {collection_name}")

        except Exception as e:
            Logger().info(f"Error uploading logs to Firestore: {e}")
'''
    def upload_logs_with_timestamps(log_data, collection_name, document_name):
"""
주어진 로그 데이터를 Firestore에 업로드하며, time_range 내 날짜를 Timestamp로 변환.

Args:
log_data (dict): Firestore에 업로드할 데이터 딕셔너리.
collection_name (str): Firestore 컬렉션 이름.
document_name (str): Firestore 문서 이름.
"""
        try:
# 날짜 문자열을 datetime으로 변환 후 Timestamp로 변환
            time_range = log_data.get('time_range', {})
            start_time_str = time_range.get('start_time')
            end_time_str = time_range.get('end_time')

# 문자열을 datetime으로 변환 (포맷: "Month-Day-Year")
            start_time = datetime.strptime(start_time_str, "%B-%d-%Y") if start_time_str else None
            end_time = datetime.strptime(end_time_str, "%B-%d-%Y") if end_time_str else None

# Firestore Timestamp로 변환
            if start_time:
                log_data['time_range']['start_time'] = firestore.firestore.Timestamp.from_datetime(start_time)
            if end_time:
                log_data['time_range']['end_time'] = firestore.firestore.Timestamp.from_datetime(end_time)

# Firestore에 데이터 업로드
            doc_ref = db.collection(collection_name).document(document_name)
            doc_ref.set(log_data)
            print(f"Logs successfully uploaded to Firestore: {collection_name}/{document_name}")

        except Exception as e:
        print(f"Error uploading logs to Firestore: {e}")
'''
