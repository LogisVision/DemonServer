import paho.mqtt.client as mqtt
import os

#######

from SCSCtrl import TTLServo

servoPos_1 = 0  # Pan position of the camera.
servoPos_5 = 0  # The vertical position of the camera.


def limitCtl(maxInput, minInput, rawInput):
    if rawInput > maxInput:
        limitBuffer = maxInput
    elif rawInput < minInput:
        limitBuffer = minInput
    else:
        limitBuffer = rawInput

    return limitBuffer


def cameraUp():
    global servoPos_5  # Global variables declaration
    servoPos_5 = limitCtl(25, -40, servoPos_5-15)
    TTLServo.servoAngleCtrl(5, servoPos_5, 1, 150)

def cameraDown():
    global servoPos_5  # Global variables declaration
    servoPos_5 = limitCtl(25, -40, servoPos_5+15)
    TTLServo.servoAngleCtrl(5, servoPos_5, 1, 150)

# Camera turn right
def ptRight():
    global servoPos_1
    servoPos_1 = limitCtl(80, -80, servoPos_1+15)
    TTLServo.servoAngleCtrl(1, servoPos_1, 1, 150)

# Camera turn left
def ptLeft():
    global servoPos_1
    servoPos_1 = limitCtl(80, -80, servoPos_1-15)
    TTLServo.servoAngleCtrl(1, servoPos_1, 1, 150)

#######

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")
    if message.payload.decode() == "turn_on_camera":
        # 카메라를 켜는 명령어 (예: libcamera-still 사용)
        os.system("libcamera-still -o image.jpg")  # 예시로 사진을 촬영하는 코드
        print("Camera has been triggered!")
        ptLeft();
        

client = mqtt.Client()
client.on_message = on_message
client.connect("70.12.227.160")  # 라즈베리 파이의 IP 주소
client.subscribe("commands/camera")

client.loop_forever()
