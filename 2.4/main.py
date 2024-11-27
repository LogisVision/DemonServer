from utils.mqtt_handler import MQTTHandler
from utils.firebase_handler import FirebaseHandler
from utils.chatgpt_logger_analyzer import LogAnalyzer
from utils.logger import Logger
from datetime import datetime, timezone, timedelta
import pytz 
import time

def main_loop():
    # 설정
    broker_address = "localhost"
    '''
    sub_topic = "A/Demon/Result"
    pub_topic = "A/Demon/Command"
    status_request_topic = "A/Demon/Status/ToJetbot"
    status_response_topic = "A/Demon/Status/ToDemon"
    statusA_request_topic = "A/Demon/Status/ToJetbot"
    statusB_request_topic = "B/Demon/Status/ToJetbot"
    statusA_response_topic = "A/Demon/Status/ToDemon"
    statusB_response_topic = "B/Demon/Status/ToDemon"
    '''

    pub_topic = [
        ("A/Demon/Command", 0), 
        ("B/Demon/Command", 0), 
        ("A/Demon/Status/ToJetbot", 0),
        ("B/Demon/Status/ToJetbot", 0)]
    sub_topic = [
        ("A/Demon/Result", 0),
        ("B/Demon/Result", 0),
        ("A/Demon/Status/ToDemon", 0), 
        ("B/Demon/Status/ToDemon", 0) ]

    # Firebase 설정
    credential_path = "./data/logis_vision.json"
    collection_name = "commands"
    robots = {"A", "B"}
    is_requested = "request"
    local_tz = pytz.timezone('Asia/Seoul')
    

    # 명령 메시지 예시
    # FirebaseHandler 객체 생성
    firebase_handler = FirebaseHandler(credential_path, collection_name)

    Logger().info("firebase_handler is set")

    # MQTTHandler 객체 생성
    mqtt_handler = MQTTHandler(
        broker_address,
        sub_topic,
        pub_topic,
#status_request_topic,
#status_response_topic
    )

    Logger().info("mqtt_hander is set")

    log_analyzer = LogAnalyzer()
    last_summary_time = datetime.now(local_tz)
                              
    log_summary_interval = 60
    log_path = "./app.log"

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
                received_id = mqtt_handler.get_id()
                print(received_id)
                if received_id:
                    firebase_handler.unlock_data("A", received_id)
                if sorted_data:
                    for command in sorted_data:
                        is_True = mqtt_handler.check_status(robot_type)
                        if is_True:
                            mqtt_handler.send_command(command, robot_type)
                            outer_id = command.get('id')
                            firebase_handler.to_progress(outer_id)
                else:
                    Logger().warning("No data matching the criteria was found.")

            current_time = datetime.now(local_tz)

            if current_time - last_summary_time >= timedelta(seconds=log_summary_interval):
                log_data = log_analyzer.read_log_file(log_path, last_summary_time, current_time)
                Logger().info("Perfoming log summary...")
# 로그 데이터가 존재할 때
                if log_data:
                    response_content = log_analyzer.summarize_logs(log_data)
					# json 형태로 정리(dict)
                    log_data = log_analyzer.save_response_to_json(response_content)
                    firebase_handler.upload_logs_with_timestamps(log_data, "logs")
                    Logger().info("Log summary completed and uploaded")
                else:
                    Logger().warning("No logs available for summarization")

                last_summary_time = current_time

            Logger().debug("Retrying in 5 seconds...")
            time.sleep(5)  # 유지
    except KeyboardInterrupt:
        Logger().critical("\nProgram interrupted by user.")
    finally:
        # MQTT 종료
        mqtt_handler.stop()
        
# main_loop
if __name__ == "__main__":
    main_loop()
