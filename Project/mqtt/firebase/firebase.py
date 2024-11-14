import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
from firebase_admin.firestore import SERVER_TIMESTAMP
from google.cloud.firestore_v1 import DocumentReference

import asyncio
import time

# Firebase 초기화
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-firebase-app-id.appspot.com'
})

# Firestore와 Storage 초기화
db = firestore.client()
bucket = storage.bucket()

# API 정의
class LOGIS_API:
    
    class ItemAPI:
        
        @staticmethod
        async def get_image_data(file_name):
            extensions = ["png", "jpg", "jpeg", "gif"]
            for extension in extensions:
                blob = bucket.blob(f"picture/{file_name}.{extension}")
                if blob.exists():
                    return blob.generate_signed_url(expiration=3600)  # URL expires in 1 hour
            print("[Error] 이미지 파일을 찾을 수 없습니다.")
            return None
        
        @staticmethod
        async def mod_data(item):
            try:
                # 이미지 URL 가져오기
                image_url = await LOGIS_API.ItemAPI.get_image_data(item.get("file_name"))
                # 색상 HEX 변환
                color = item.get("color", {})
                color_hex = f"#{color.get('red', 0):02X}{color.get('green', 0):02X}{color.get('blue', 0):02X}"

                # 위치 데이터 가져오기
                location_ref = item.get("location")
                if location_ref:
                    location_snap = location_ref.get()
                    if location_snap.exists:
                        location_data = location_snap.to_dict()
                        return {
                            "id": item.get("id"),
                            "location_data": location_data,
                            "color_hex": color_hex,
                            "file_name": item.get("file_name"),
                            "image_url": image_url,
                            "state": item.get("state")
                        }
                    else:
                        print("[Error] 위치 정보를 찾을 수 없습니다.")
                        return 404
            except Exception as e:
                print(f"[Error] {e}")
                return None
        
        @staticmethod
        async def get_one(item_id):
            item_ref = db.collection("items").document(item_id)
            item_snapshot = item_ref.get()
            if item_snapshot.exists:
                item = item_snapshot.to_dict()
                item["id"] = item_id
                return await LOGIS_API.ItemAPI.mod_data(item)
            print("[Error] 아이템을 찾을 수 없습니다.")
            return 404

        # 이외의 메소드들도 Firebase 관련 코드로 작성
        # 예: add(), update(), delete()

    class IncomingAPI:
        @staticmethod
        async def get_one(incoming_id):
            incoming_ref = db.collection("incomings").document(incoming_id)
            incoming_snapshot = incoming_ref.get()
            if incoming_snapshot.exists:
                incoming = incoming_snapshot.to_dict()
                incoming["id"] = incoming_id
                # 관련 아이템 데이터 가져오기
                if "item" in incoming:
                    item_data = await LOGIS_API.ItemAPI.get_one(incoming["item"].id)
                    incoming["item_data"] = item_data
                return incoming
            print("[Error] 해당 입고라인 데이터를 찾을 수 없습니다.")
            return 404

        # 나머지 메소드 작성
        # 예: getAll(), updateState(), addItem()

    class CommandAPI:
        
        @staticmethod
        async def get_all():
            commands = db.collection("commands").stream()
            commands_data = []
            for command in commands:
                data = command.to_dict()
                data["id"] = command.id
                if "forward" in data:
                    forward_ref = data["forward"]
                    forward_snapshot = forward_ref.get()
                    if forward_snapshot.exists:
                        data["forward_data"] = forward_snapshot.to_dict()
                commands_data.append(data)
            return commands_data

        # 나머지 메소드 작성
        # 예: getRequested(), getTargetOne(), update()

# 실행 예시
async def main():
    api = LOGIS_API()
    result = await api.ItemAPI.get_one("some-item-id")
    print(result)

# Async로 main 함수를 실행
asyncio.run(main())
