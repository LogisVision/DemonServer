import paho.mqtt.client as mqtt
import time
from .logger import Logger
from datetime import datetime
import json

class MQTTHandler:
    def __init__(self, broker_address, sub_topic, pub_topic):
        self.broker_address = broker_address
        self.sub_topic = sub_topic
        self.pub_topic = pub_topic

        self.statusA_request_topic = "A/Demon/Status/ToJetbot"
        self.statusB_request_topic = "B/Demon/Status/ToJetbot"
        self.statusA_response_topic = "A/Demon/Status/ToDemon"
        self.statusB_response_topic = "B/Demon/Status/ToDemon"

        self.command_topic_A = "A/Demon/Command"
        self.result_topic_A = "A/Demon/Result"

        self.command_topic_B = "B/Demon/Command"
        self.result_topic_B = "B/Demon/Result"

        self.jetsonA_status = "unknown"
        self.jetsonB_status = "unknown"
        self.client = mqtt.Client()
        self.received_id = None

        # 콜백 함수 등록
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    @staticmethod
    def log_time():
        """현재 시간 기록용 함수"""
        return datetime.now().strftime("[%Y|%m|%d %H:%M:%S]")

    @staticmethod
    def validate_received_message(message_payload):
        """수신 메시지 유효성 검사"""
        if not message_payload.strip():
            print(f"{MQTTHandler.log_time()} Error: Received empty message!")
            return False
        return True

    def on_connect(self, client, userdata, flags, rc):
        """브로커 연결 시 호출되는 콜백"""
        if rc == 0:
            Logger().info(f"Connected to MQTT broker: {self.broker_address}")
            # 연결되면 구독 설정
            client.subscribe(self.sub_topic)
#            client.subscribe(self.status_response_topic)
#            client.subscribe(self.statusA_response_topic)
#            client.subscribe(self.statusB_response_topic)

            Logger().info(f"Subscribed to topics: {self.sub_topic}")
        else:
            Logger().warning(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, message):
        """메시지 수신 시 호출되는 콜백"""
        message_payload = message.payload.decode("utf-8")
        topic = message.topic
        print(topic)
        Logger().info(f"Received message from topic '{topic}': {message_payload}")

        
        if topic == self.statusA_response_topic:
            self.jetsonA_status = message_payload
            Logger().info(f"Updated Jetson_A status: {self.jetsonA_status}")
        elif topic == self.statusB_response_topic:
            self.jetsonB_status = message_payload
            Logger().info(f"Updated Jetson_B status: {self.jetsonA_status}")
            
        elif topic == self.result_topic_B:
            self.received_id = message_payload
            Logger().info(f"Message on sub_topic: {message_payload}")


    def start(self):
        """MQTT 클라이언트 시작"""
        print("!")
        self.client.connect(self.broker_address)
        self.client.loop_start()
        Logger().info(f"MQTT loop started")

    def stop(self):
        """MQTT 클라이언트 정지"""
        self.client.loop_stop()
        self.client.disconnect()
        Logger().info(f"MQTT client stopped")

    def check_status(self, robot_type):
        """젯슨 상태 확인 후 명령 전송"""
        if robot_type == "A":
            result = self.client.publish(self.statusA_request_topic, "request_status")  # 상태 요청
            time.sleep(1)
            if self.jetsonA_status == "waiting":
                Logger().info(f"Robot {robot_type} is idle")
                return True

        elif robot_type == "B":
            time.sleep(1)
            self.client.publish(self.statusB_request_topic, "request_status")  # 상태 요청
            if self.jetsonB_status == "waiting":
                Logger().info(f"Robot {robot_type} is idle")
                return True
                
        else:
            Logger().warning(f"Cannot send command. Both Jetsons are not idle.")
            Logger().warning(f"A : {self.jetsonA_status}.B : {self.jetsonB_status}")
            return None

    def send_command(self, command_message, robot_type):
        """젯슨 상태 확인 후 명령 전송"""
        if robot_type == 'A':
            json_data = json.dumps(command_message)
            result = self.client.publish(self.command_topic_A, json_data)
            Logger().info(f"Command sent to A: {json_data}")

        elif robot_type == "B":
            json_data = json.dumps(command_message)
            self.client.publish(self.command_topic_B, json_data)
            Logger().info(f"Command sent to B: {json_data}")
                
        else:
            Logger().warning(f"Cannot send command. Both Jetsons are not idle.")
            Logger().warning(f"A : {self.jetsonA_status}.B : {self.jetsonB_status}")

    def get_id(self):
        """수신된 메시지를 반환"""
        received_id = self.received_id
        self.received_id = None  # 메시지를 가져온 후 초기화
        Lgoger().info(f"received_id : {received_id}")
        return received_id

