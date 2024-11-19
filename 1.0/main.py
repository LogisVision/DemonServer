#from firebase import fetch_and_sort_data
#from mqtt import publication 
from utils import fetch_and_sort_data, chat_loop
from var import sub_topic, pub_topic #sub_topic과 pub_topic 주소
from var import robot_type, is_requested

print(robot_type, is_requested)
while True:
    # firebase에서 데이터 가져오기
    sorted_data = fetch_and_sort_data(robot_type, is_requested)

    # mqtt로 데이터 출력하기
    chat_loop(sorted_data)
