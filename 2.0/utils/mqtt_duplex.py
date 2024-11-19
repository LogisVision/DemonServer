import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json

broker_address = "localhost"  # 라즈베리 파이 ip 주소
sub_topic = "test/response"  # jetson nano에서 발행한 메시지를 구독할 토픽
pub_topic = "test/topic"  # jetson nano으로 명령을 보내는 토픽

# 젯슨 나노의 상태를 체크하기 위한 topic
status_request_topic = "jetson/request_status"
status_response_topic = "jetson/status_response"

jetson_status = "unknown"

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
    global jetson_status
    message_payload = message.payload.decode("utf-8")
    topic = message.topic
    print(topic)

    #print(f"{log_time()} Received status response: {jetson_status}")
    if topic == status_response_topic:
        jetson_status = message_payload
        print(f"Update Jetson status:  {jetson_status}")
        time.sleep(1)

    elif topic == sub_topic:
        print(f"Message : {message_payload}")


    # 예시로 응답 메시지 발행
#    response_message = "Message received on Raspberry Pi"
#    client.publish(pub_topic, response_message)

def chat_loop(command_message):
    global jetson_status
    current_time = log_time()
    # 메시지 수신 콜백 함수

    # MQTT 클라이언트 생성 및 브로커 연결
    client = mqtt.Client()
    client.connect(broker_address)


    # 토픽 구독 및 콜백 함수 설정
    client.subscribe(sub_topic)
    client.subscribe(status_response_topic)
    client.on_message = on_message
    client.publish(status_request_topic, "request_status")
    #client.message_callback_add(status_response_topic, on_status_response)

    # 메시지 수신 루프 시작
    client.loop_start()
    time.sleep(2)  # 5초 간격으로 송신
    try:
        if jetson_status == "idle":
            json_data = json.dumps(command_message)
            client.publish(pub_topic, json_data)
            print(f"{log_time()}Command sent")
            time.sleep(1)

                # 송신 간격을 위해 잠시 대기
        else:
            print("jetson nano is not idle, Current status:{jetson_status}")
            
    except KeyboardInterrupt:
        # 프로그램 종료 시 MQTT 루프 중지
        client.loop_stop()

    finally:
        client.loop_stop()
        client.disconnect()
