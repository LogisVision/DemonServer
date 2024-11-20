import firebase_admin
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
            Logger.print_with_time("Skipping invalid document: Missing required keys")
            return None

        if data.get("robot") != robot_type or data.get("state") != is_requested:
            return None

        return data

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
                Logger.print_with_time("No valid data found matching the criteria.")
                return []

            # datetime을 기준으로 정렬
            filtered_data.sort(key=lambda x: x["datetime"])

            # 필요한 키만 추출
            keys_to_extract = ["destination", "state", "robot", "item"]
            extracted_data = [self.extract_keys(data, keys_to_extract) for data in filtered_data]

            # 정렬된 데이터 출력
#            for data in extracted_data:
#                self.print_data(data)

            return extracted_data

        except Exception as e:
            Logger.print_with_time(f"Error fetching data from Firebase: {e}")
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
                if doc.id == command_id and data["state"] == "request":
                    doc.reference.update({"state" : "completed", })
                    Logger.print_with_time(f"Updated 'state' for document {doc.id} to completed")
                elif 'forward' in data and data["state"] == "lock":
                    forward_path = data["forward"].path.split('/',1)[1]
                    if forward_path == command_id:
                        doc.reference.update({"state" : "request", })
                        Logger.print_with_time(f"Updated 'state' for document {doc.id} to request")
        except Exception as e:
            Logger.print_with_time(f"Error fetching data from Firebase: {e}")
            return []
