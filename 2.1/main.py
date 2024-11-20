from utils.mqtt_handler import MQTTHandler
from utils.firebase_handler import FirebaseHandler
from utils.logger import Logger
import time

def main_loop():
    # 설정
    broker_address = "localhost"
    sub_topic = "test/response"
    pub_topic = "test/topic"
    status_request_topic = "jetson/request_status"
    status_response_topic = "jetson/status_response"

    # Firebase 설정
    credential_path = "./data/logis_vision.json"
    collection_name = "commands"
    robot_type = "B"
    is_requested = "completed"
    

    # 명령 메시지 예시
    # FirebaseHandler 객체 생성
    firebase_handler = FirebaseHandler(credential_path, collection_name)

    tprint = Logger.print_with_time
    tprint("firebase_hander is set")

    # MQTTHandler 객체 생성
    mqtt_handler = MQTTHandler(
        broker_address,
        sub_topic,
        pub_topic,
        status_request_topic,
        status_response_topic
    )

    tprint("mqtt_hander is set")
    while True:
        tprint("Building mqtt connection...")
        try:
            # MQTT 시작
            mqtt_handler.start()
            break;
        except Exception as e:
            tprint(f"Error Occured: {e} ")

        # 명령 전송

    try:
        # 프로그램 지속 실행 (테스트용)
        while True:
            tprint("Trying to fetch and send command...")
            time.sleep(1)
            sorted_data = firebase_handler.fetch_and_sort_data(robot_type, is_requested)
            locked_data = firebase_handler.fetch_and_sort_data(robot_type, is_requested)
            if sorted_data:
                tprint("Fetched and sorted data successfully!")
                command = sorted_data[0]
                mqtt_handler.send_command(command)
            else:
                tprint("No data matching the criteria was found.")

            tprint("Retrying in 5 seconds...")
            time.sleep(5)  # 유지
    except KeyboardInterrupt:
        tprint("\nProgram interrupted by user.")
    finally:
        # MQTT 종료
        mqtt_handler.stop()
        
# main_loop
if __name__ == "__main__":
    main_loop()
