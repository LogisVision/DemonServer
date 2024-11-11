import asyncio
import websockets

async def send_commands():
    uri = "ws://70.12.225.97:8765"  # Jetson Nano의 IP 주소로 설정
    async with websockets.connect(uri) as websocket:
        while True:
            # 보낼 명령어를 입력받기
            command = input("서버로 보낼 명령을 입력하세요 (종료하려면 'exit' 입력): ")
            
            if command.lower() == 'exit':
                print("명령 전송을 종료합니다.")
                break
            
            # 명령어 서버로 전송
            await websocket.send(command)
            print(f"보낸 명령: {command}")
            
            # 서버의 응답 수신
            response = await websocket.recv()
            print(f"서버로부터 응답: {response}")

# Python 3.6 호환: asyncio.run() 없이 직접 이벤트 루프 실행
loop = asyncio.get_event_loop()
loop.run_until_complete(send_commands())

