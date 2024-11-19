import paho.mqtt.client as mqtt

import json

broker_address = "70.12.227.160"  # Raspberry Pi IP
sub_topic = "test/topic"  # 구독할 토픽
pub_topic = "test/response"  # 발행할 토픽

status_request_topic = "jetson/request_status"
status_response_topic = "jetson/status_response"

jetson_status = "idle"
# 메시지 수신 콜백 함수
def on_message(client, userdata, message):
	if message.topic == status_request_topic:
		client.publish(status_response_topic, jetson_status)
		print("request accepted")

	elif message.topic == sub_topic:
		json_data= message.payload.decode("utf-8")
		received_message = json.loads(json_data)
		print(type(received_message))
		print(f"Message Received from Raspberry Pi: {received_message}")
		response_message = f"Message '{received_message}' received on Mac"

    # 예시로 응답 메시지 발행

# MQTT 클라이언트 생성 및 브로커 연결
client = mqtt.Client()
client.connect(broker_address)

# 토픽 구독 및 콜백 함수 설정
client.subscribe(sub_topic)
client.subscribe(status_request_topic)
client.on_message = on_message

# 메시지 수신 루프를 백그라운드에서 실행
client.loop_start()

# 사용자 입력을 받아서 메시지 발행
try:
    while True:
        message = input("Enter message to publish (or type 'exit' to quit): ")
        if message.lower() == "exit":
            break
        client.publish(pub_topic, message)
        print(f"Message '{message}' sent to topic '{pub_topic}'")

finally:
    client.loop_stop()
    client.disconnect()

