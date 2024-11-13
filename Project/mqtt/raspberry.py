import paho.mqtt.client as mqtt

broker_address = "localhost"  # 라즈베리 파이 IP 주소
topic = "commands/camera"

client = mqtt.Client()
client.connect(broker_address)

# 카메라를 켜라는 메시지 전송
client.publish(topic, "turn_on_camera")
print("Message sent to turn on the camera.")
