import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json

class MQTTHandler:
    def __init__(self, broker_address, sub_topic, pub_topic, status_request_topic, status_response_topic):
        self.broker_address = broker_address
        self.sub_topic = sub_topic
        self.pub_topic = pub_topic
        self.status_request_topic = status_request_topic
        self.status_response_topic = status_response_topic

        self.jetson_status = "unknown"
        self.client = mqtt.Client()

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
            print(f"{self.log_time()} Connected to MQTT broker: {self.broker_address}")
            # 연결되면 구독 설정
            client.subscribe(self.sub_topic)
            client.subscribe(self.status_response_topic)
            print(f"{self.log_time()} Subscribed to topics: {self.sub_topic}, {self.status_response_topic}")
        else:
            print(f"{self.log_time()} Failed to connect, return code {rc}")

    def on_message(self, client, userdata, message):
        """메시지 수신 시 호출되는 콜백"""
        message_payload = message.payload.decode("utf-8")
        topic = message.topic
        print(f"{self.log_time()} Received message from topic '{topic}': {message_payload}")

        if topic == self.status_response_topic:
            self.jetson_status = message_payload
            print(f"{self.log_time()} Updated Jetson status: {self.jetson_status}")
        elif topic == self.sub_topic:
            print(f"{self.log_time()} Message on sub_topic: {message_payload}")

    def start(self):
        """MQTT 클라이언트 시작"""
        self.client.connect(self.broker_address)
        self.client.loop_start()
        print(f"{self.log_time()} MQTT loop started")

    def stop(self):
        """MQTT 클라이언트 정지"""
        self.client.loop_stop()
        self.client.disconnect()
        print(f"{self.log_time()} MQTT client stopped")

    def send_command(self, command_message):
        """젯슨 상태 확인 후 명령 전송"""
        self.client.publish(self.status_request_topic, "request_status")  # 상태 요청
        time.sleep(1)  # 상태 응답 대기

        if self.jetson_status == "idle":
            json_data = json.dumps(command_message)
            self.client.publish(self.pub_topic, json_data)
            print(f"{self.log_time()} Command sent: {json_data}")
        else:
            print(f"{self.log_time()} Cannot send command. Jetson is not idle: {self.jetson_status}")
