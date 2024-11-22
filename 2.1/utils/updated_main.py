from utils.mqtt_handler import MQTTHandler
from utils.firebase_handler import FirebaseHandler
from utils.logger import Logger
import time

# Logger instance
logger = Logger()

def main_loop():
    broker_address = "localhost"
    sub_topic = "test/response"
    pub_topic = "test/topic"
    status_request_topic = "jetson/request_status"
    status_response_topic = "jetson/status_response"

    credential_path = "./data/logis_vision.json"
    collection_name = "commands"
    robot_type = "B"
    is_requested = "completed"

    # Firebase setup
    firebase_handler = FirebaseHandler(credential_path, collection_name)
    logger.info("FirebaseHandler is set")

    # MQTT setup
    mqtt_handler = MQTTHandler(
        broker_address,
        sub_topic,
        pub_topic,
        status_request_topic,
        status_response_topic,
    )
    logger.info("MQTTHandler is set")

    while True:
        logger.info("Building MQTT connection...")
        try:
            mqtt_handler.start()
            break
        except Exception as e:
            logger.error(f"Error occurred: {e}")

    try:
        while True:
            logger.info("Trying to fetch and send command...")
            time.sleep(1)
            sorted_data = firebase_handler.fetch_and_sort_data(robot_type, is_requested)
            if sorted_data:
                logger.info("Fetched and sorted data successfully!")
                command = sorted_data[0]
                mqtt_handler.send_command(command)
            else:
                logger.info("No data matching the criteria was found.")
            logger.info("Retrying in 5 seconds...")
            time.sleep(5)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user.")
    finally:
        mqtt_handler.stop()

if __name__ == "__main__":
    main_loop()
