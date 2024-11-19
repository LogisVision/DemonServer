import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json

broker_address = "localhost"  # 라즈베리 파이 ip 주소
sub_topic = "test/response"  # jetson nano에서 발행한 메시지를 구독할 토픽
pub_topic = "test/topic"  # jetson nano으로 명령을 보내는 토픽

# 시간 기록용 함수
def log_time():
    current_time = datetime.now().strftime("[%Y|%m|%d %H:%M:%S]")
    return current_time

def validate_received_message(message_payload):
    if not message_payload.strip():
        error_time = log_time()
        print(f"{error_time}Error: Received empty message!")
        return False

    else:
        return True
        
def on_message(client, userdata, message):
    message_payload = message.payload.decode()
    if not validate_received_message(message_payload):
        return
    message_time = log_time()
    print(f"{message_time}Received : {message_payload}")


    # 예시로 응답 메시지 발행
#    response_message = "Message received on Raspberry Pi"
#    client.publish(pub_topic, response_message)

def chat_loop(command_message):

    current_time = log_time()
    # 메시지 수신 콜백 함수

    # MQTT 클라이언트 생성 및 브로커 연결
    client = mqtt.Client()
    client.connect(broker_address)

    # 토픽 구독 및 콜백 함수 설정
    client.subscribe(sub_topic)
    client.on_message = on_message

    # 메시지 수신 루프 시작
    client.loop_start()

    json_data = json.dumps(command_message)
    try:
            # 송신할 메시지
#            command_message = input("Enter message to publish(or type 'exit' to quit):")
#            if command_message.lower() == "exit":
#                break;
        client.publish(pub_topic, json_data)
        print(f"{current_time}Command sent")

            # 송신 간격을 위해 잠시 대기
        time.sleep(5)  # 5초 간격으로 송신
    except KeyboardInterrupt:
        # 프로그램 종료 시 MQTT 루프 중지
        client.loop_stop()
