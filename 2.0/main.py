from utils.module import MQTTHandler
from utils.firebase_handler import FirebaseHandler
import time

if __name__ == "__main__":
    # 설정
    broker_address = "localhost"
    sub_topic = "test/response"
    pub_topic = "test/topic"
    status_request_topic = "jetson/request_status"
    status_response_topic = "jetson/status_response"

    # Firebase 설정
    credential_path = "./data/logis_vision.json"
    collection_name = "commands"
    robot_type = "A"
    is_requested = "completed"

    # 명령 메시지 예시
    command_message = {"action": "move", "x": 10, "y": 20}

    # FirebaseHandler 객체 생성
    firebase_handler = FirebaseHandler(credential_path, collection_name)

    # MQTTHandler 객체 생성
    mqtt_handler = MQTTHandler(
        broker_address,
        sub_topic,
        pub_topic,
        status_request_topic,
        status_response_topic
    )

    try:
        # MQTT 시작
        mqtt_handler.start()

        # 명령 전송

        # 프로그램 지속 실행 (테스트용)
        while True:
            sorted_data = firebase_handler.fetch_and_sort_data(robot_type, is_requested)
            if sorted_data:
                print("Fetched and sorted data successfully!")
                mqtt_handler.send_command(command_message)
            else:
                print("No data matching the criteria was found.")

        time.sleep(1)  # 유지
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        # MQTT 종료
        mqtt_handler.stop()
