#from firebase import fetch_and_sort_data
#from mqtt import publication 
from utils import fetch_and_sort_data, chat_loop, on_message
from var import sub_topic, pub_topic #sub_topic과 pub_topic 주소

# firebase에서 데이터 가져오기
sorted_data = fetch_and_sort_data()

# mqtt로 데이터 출력하기
chat_loop()
