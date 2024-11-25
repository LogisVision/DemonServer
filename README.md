# Logis Vision Demon Server

## 프로젝트 개요

![Logis_Vision_Logo](https://raw.githubusercontent.com/LogisVision/Logis_Platform/refs/heads/master/Basic%20Theme%403x.png)

**"Logis Vision"** 은 두 대의 AGV(Jetson Nano)를 이용한 통합 물류 관리 솔루션으로,
입고된 상품을 자동으로 등록하고 관리자 지정 위치로 이동시킵니다.

**"Logis Vision Demon Server"** 는 Web Platform에서 제공한 명령어가 Firebase를 통해 업로드 되면,
주기적인 Polling으로 변경 사항을 추적하여 새로운 명령어가 있는지 확인합니다.
그리고 AGV와 통신하여 명령어를 전달하고, AGV의 상태와 명령어 완수 여부를 Firebase에 업데이트합니다.

# 프로젝트 개요
- 해당 프로젝트는 라즈베리 파이를 이용하여 mqtt 브로커 역할을 맡기고, 동시에 firebase의 cloud store database의 자료를 실시간으로 받아와 jetson nano 보드에 명령을 전송하기 위해 mqtt 통신을 이용하는 일련의 과정을 위한 프로젝트입니다.

## 프로젝트 구조
- 해당 프로젝트는 main.py 파일을 구동하면 하부 디렉토리의 모듈을 import하여 동작하는 구조로 제작되었습니다.

## 기본 디렉토리
### main.py
- utils에 존재하는 모듈 함수들을 호출하여 실행하는 역할을 하는 python 파일
### var.py
- main.py에서 구동할 때 필요한 mqtt 주소 같은 변수들을 저장할 파일

## utils 디렉토리
### firebase_handler.py
- firebase에 있는 commands db를 읽어와 유효한 명령을 AGV에게 전달하는 과정
- 해당 명령에 대한 실행 결과를 돌려 받고 db에 있는 데이터를 수정하는 과정
- 마지막으로 일정 시간동안 발행한 로그를 요약한 정보를 다시 업로드하는 과정
### logger.py
- 실행하면서 일어난 모든 로그를 터미널에서 출력함과 동시에 기본 디렉토리의 app.log 파일에 기록하는 모듈
- 로그 레벨에 따라 debug, info, warning, error, critical의 5단계로 나누어 기록함
### mqtt_handler.py
- mqtt에서 동작하는 함수들을 모듈화한 파일
- mqtt를 이용하여 라즈베리파이와 AGV간 통신을 담당하는 브로커 역할을 수행하게함
- 통신을 통해 AGV의 상태를 확인하고 명령 전달 및 답을 수신하는 역할 
### chatgpt_logger_analyzer.py
- main문을 실행하면서 일어난 로그들을 일정 시간 단위로 chatgpt_api를 이용해 로그를 요약하고 요약한 내용을 firebase에 올릴 수 있도록함
- 받은 응답을 json 형태로 올릴 수 있도록 정리하여 firebase_handler와 유기적으로 작동함

## data 디렉토리
- 실제 작동 시 firebase 프로젝트의 key json 파일이 위치하는 장소


