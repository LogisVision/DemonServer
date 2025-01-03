from utils.mqtt_handler import MQTTHandler
from utils.firebase_handler import FirebaseHandler
from utils.logger import Logger
import time

def main_loop():
    # 설정
    broker_address = "localhost"
    sub_topic = "test/response"
    pub_topic = "test/topic"
    status_request_topic = "A/Demon/Status/ToJetbot"
    status_response_topic = "A/Demon/Status/ToDemon"
    statusA_request_topic = "A/Demon/Status/ToJetbot"
    statusB_request_topic = "B/Demon/Status/ToJetbot"
    statusA_response_topic = "A/Demon/Status/ToDemon"
    statusB_response_topic = "B/Demon/Status/ToDemon"

    # Firebase 설정
    credential_path = "./data/logis_vision.json"
    collection_name = "commands"
    robots = {"A", "B"}
    is_requested = "request"
    

    # 명령 메시지 예시
    # FirebaseHandler 객체 생성
    firebase_handler = FirebaseHandler(credential_path, collection_name)

    Logger().info("firebase_hander is set")

    # MQTTHandler 객체 생성
    mqtt_handler = MQTTHandler(
        broker_address,
        sub_topic,
        pub_topic,
        status_request_topic,
        status_response_topic
    )

    Logger().info("mqtt_hander is set")
    while True:
        Logger().info("Building mqtt connection...")
        try:
            # MQTT 시작
            mqtt_handler.start()
            break;
        except Exception as e:
            Logger(),error(f"Error Occured: {e} ")

        # 명령 전송

    try:
        # 프로그램 지속 실행 (테스트용)
        while True:
            Logger().info("Trying to fetch and send command...")
            time.sleep(1)
            for robot_type in robots:
                sorted_data = firebase_handler.fetch_and_sort_data(robot_type, is_requested)
                locked_data = firebase_handler.fetch_and_sort_data(robot_type, is_requested)
                if sorted_data:
                    for command in sorted_data:
                        is_True = mqtt_handler.check_status(robot_type)
                        if is_True:
                            mqtt_handler.send_command(command, robot_type)
                            outer_id = command.get('id')
                            print(outer_id)
                            firebase_handler.to_progress(outer_id)
                else:
                    Logger().warning("No data matching the criteria was found.")

            Logger().info("Retrying in 5 seconds...")
            time.sleep(5)  # 유지
    except KeyboardInterrupt:
        Logger().critical("\nProgram interrupted by user.")
    finally:
        # MQTT 종료
        mqtt_handler.stop()
        
# main_loop
if __name__ == "__main__":
    main_loop()
