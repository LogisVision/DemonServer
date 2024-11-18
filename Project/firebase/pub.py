import paho.mqtt.client as mqtt
import fetch

broker_address = "localhost"  # 라즈베리 파이 IP 주소
sub_topic = "test/response"  # 맥에서 발행한 메시지를 구독할 토픽
pub_topic = "test/topic"  # 맥으로 명령을 보내는 토픽

sorted_data = fetch.fetch_and_sort_data()
print(sorted_data)

# 메시지 수신 콜백 함수
def on_message(client, userdata, message):
    print(f"Message Received from Mac: {message.payload.decode()}")
    # 예시로 응답 메시지 발행
    response_message = "Message received on Raspberry Pi"
    client.publish(pub_topic, response_message)

# MQTT 클라이언트 생성 및 브로커 연결
client = mqtt.Client()
client.connect(broker_address)

# 토픽 구독 및 콜백 함수 설정
client.subscribe(sub_topic)
client.on_message = on_message

# 메시지 수신 루프 시작
client.loop_forever()

