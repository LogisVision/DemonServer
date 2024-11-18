import firebase_admin
from firebase_admin import credentials, firestore

# 서비스 계정 키 파일 경로를 지정해줘
cred = credentials.Certificate("./data/logis_vision.json")
firebase_admin.initialize_app(cred)

# Firestore 클라이언트 생성
db = firestore.client()

print("done db")
# Firestore 데이터 읽어오는 함수
def get_firestore_data(collection_name):
    try:
        # 지정한 컬렉션에서 문서 가져오기
        docs = db.collection(collection_name).stream()
        data = []
        for doc in docs:
            # 문서의 데이터를 딕셔너리 형태로 저장
            data.append(doc.to_dict())
            print(f"Document ID: {doc.id} => Data: {doc.to_dict()}")
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# 예제 사용
collection_name = "commands"  # 가져오려는 컬렉션 이름
data = get_firestore_data(collection_name)
