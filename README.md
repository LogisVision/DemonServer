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
### main.py
- utils에 존재하는 모듈 함수들을 호출하여 실행하는 역할을 하는 python 파일
### var.py
- main.py에서 구동할 때 필요한 mqtt 주소 같은 변수들을 저장할 파일

### utils 디렉토리
- fetch.py -> firebase에서 데이터를 받아오는 함수
- mqtt_duplex -> 라즈베리파이에서 jeston nano와 양방향 통신을 하기 위한 함수
- __init__.py -> 해당 함수들을 모듈화하기 용이하게 만들기 위한 파일

### data 디렉토리
- 실제 작동 시 firebase 프로젝트의 key json 파일이 위치하는 장소


