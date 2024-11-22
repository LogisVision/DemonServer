from .logger import Logger
import paho.mqtt.client as mqtt
import json
import time

class MQTTHandler:
    def __init__(self, broker_address, sub_topic, pub_topic, status_request_topic, status_response_topic):
        ...

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            Logger().info(f"Connected to MQTT broker: {self.broker_address}")
            client.subscribe(self.sub_topic)
            client.subscribe(self.status_response_topic)
            Logger().info(f"Subscribed to topics: {self.sub_topic}, {self.status_response_topic}")
        else:
            Logger().error(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, message):
        message_payload = message.payload.decode("utf-8")
        topic = message.topic
        Logger().info(f"Received message from topic '{topic}': {message_payload}")

        if topic == self.status_response_topic:
            self.jetson_status = message_payload
            Logger().info(f"Updated Jetson status: {self.jetson_status}")
        elif topic == self.sub_topic:
            Logger().info(f"Message on sub_topic: {message_payload}")

    def start(self):
        self.client.connect(self.broker_address)
        self.client.loop_start()
        Logger().info("MQTT loop started")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        Logger().info("MQTT client stopped")

    def send_command(self, command_message):
        self.client.publish(self.status_request_topic, "request_status")
        time.sleep(1)
        if self.jetson_status == "idle":
            json_data = json.dumps(command_message)
            self.client.publish(self.pub_topic, json_data)
            Logger().info(f"Command sent: {json_data}")
        else:
            Logger().warning(f"Cannot send command. Jetson is not idle: {self.jetson_status}")
