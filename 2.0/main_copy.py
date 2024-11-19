from utils import fetch_and_sort_data, chat_loop, var
from utils.var import sub_topic, pub_topic #sub_topic과 pub_topic 주소
from utils.var import robot_type, is_requested
from utils.var import status_request_topic, status_response_topic

if __name__ == "__main__":
    while True:
        # firebase에서 데이터 가져오기
        sorted_data = fetch_and_sort_data(robot_type, is_requested)

        # mqtt로 데이터 출력하기
        chat_loop(sorted_data)
