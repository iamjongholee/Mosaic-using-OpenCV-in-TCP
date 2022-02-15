import socket
import select

server_port = 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #소켓을 생성
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #소켓 옵션 설정
server_socket.bind(('127.0.0.1', server_port)) #호스트와 포트를 바인딩

file_name_1_pixel = "mosaic_1_pixel.jpg" #파일 이름을 설정
file_name_2_blur = "mosaic_2_blur.jpg"
fd = open(file_name_1_pixel, 'wb') #파일을 열고 해당 파일 객체를 반환, wb:쓰기용으로 열기+바이너리 모드
fd = open(file_name_2_blur, 'wb')

while True:
    ready = select.select([server_socket], [], [], 5) #입출력을 위한 대기, 준비된 객체 리스트 반환
    print(ready)
    if ready[0]:
        recv_data, recv_addr = server_socket.recvfrom(1024) #소켓으로부터 데이터를 수신
        fd.write(recv_data) #파일 객체에 데이터를 입력
    else: #모자이크 작업이 완료되면 어떤 파일로 저장되었는지 출력해준다
        print("MOSAIC(pixel) completed to {}".format(file_name_1_pixel))
        print("MOSAIC(blur) completed to {}".format(file_name_2_blur))
        fd.close() #파일을 닫고 자원을 반납
        break

server_socket.close() #소켓 상태를 닫힘으로 변경