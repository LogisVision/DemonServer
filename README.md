# Logis Vision Demon Server

## 프로젝트 개요

![Logis_Vision_Logo](https://raw.githubusercontent.com/LogisVision/Logis_Platform/refs/heads/master/Basic%20Theme%403x.png)

**"Logis Vision"** 은 두 대의 AGV(Jetson Nano)를 이용한 통합 물류 관리 솔루션으로,
입고된 상품을 자동으로 등록하고 관리자 지정 위치로 이동시킵니다.

**"Logis Vision Demon Server"** 는 Web Platform에서 제공한 명령어가 Firebase를 통해 업로드 되면,
주기적인 Polling으로 변경 사항을 추적하여 새로운 명령어가 있는지 확인합니다.
그리고 AGV와 통신하여 명령어를 전달하고, AGV의 상태와 명령어 완수 여부를 Firebase에 업데이트합니다.