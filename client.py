import socket
import time
import cv2 #사용할 라이브러리 (OpenCV)

img_name_1_pixel = '../in-tong-seol/test_img_2.jpg' #둘 다 같은 이미지를 불러온다
img_name_2_blur = '../in-tong-seol/test_img_2.jpg' #파일 이름은 서버의 형식과 같게 설정함

input_pixel = input('pixel rate : ', )  # 축소 비율 입력 받기
input_blur = input('blur rate : ', )  # 블러 비율 입력 받기

rate = int(input_pixel)  # 모자이크 픽셀을 축소하여 확대할 비율
ksize = int(input_blur)  # 모자이크 블러를 처리할 정도

win_title = 'mosaic_program' #모자이크를 처리할 창 제목
img = cv2.imread('../in-tong-seol/test_img_2.jpg')
img_2 = cv2.imread('../in-tong-seol/test_img_2.jpg') #이미지 두 장 읽기

server_addr = '127.0.0.1' #호스트
server_port = 9999 #포트
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #소켓을 생성
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #소켓 옵션 설정

fd = open(img_name_1_pixel, 'rb') #파일을 열고 해당 파일 객체를 반환, rb:읽기용으로 열기+바이너리 모드
fd = open(img_name_2_blur, 'rb')
data = fd.read(1024) #파일 객체로부터 데이터를 읽어온다

while data:
    if client_socket.sendto(data, (server_addr, server_port)): #소켓에 데이터를 전송
        data = fd.read(1024) #파일 객체로부터 데이터를 읽어온다
        time.sleep(0.001)

#첫번째 모자이크 : 픽셀 축소 후 확대
while True:
    x, y, w, h = cv2.selectROI(win_title, img, False) #마우스로 작업영역 선택
    if w and h: # x,y:이미지에 / w,h:모자이크에
        roi = img[y:y+h, x:x+w] #작업영역 설정
        roi = cv2.resize(roi, (w//rate, h//rate)) # 1/rate값 의 비율로 축소한다
        roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_AREA) #원래 크기로 확대한다
        img[y:y+h, x:x+w] = roi #변경 사항을 이미지에 적용
        cv2.imshow(win_title, img) #창 띄우기
        cv2.imwrite('mosaic_1_pixel.jpg',img) #수신할 파일에 덮어씌우기
    else:
        break #끝나면 닫기

#두번째 모자이크 : 블러 처리
while True:
    x, y, w, h = cv2.selectROI(win_title, img_2, False) #마우스로 작업영역 선택
    if w > 0 and h > 0: #가로와 세로가 양수여야 영역 설정이 가능하다
        roi = img_2[y:y+h, x:x+w] #작업영역 설정
        roi = cv2.blur(roi, (ksize, ksize)) #블러 처리
        img_2[y:y+h, x:x+w] = roi #변경 사항을 이미지에 적용
        cv2.imshow(win_title, img_2) #창 띄우기
        cv2.imwrite('mosaic_2_blur.jpg',img_2) #수신할 파일에 덮어씌우기
    else:
        break #끝나면 닫기

cv2.destroyAllWindows() #cv2 종료
client_socket.close() #소켓 상태를 닫힘으로 변경
fd.close() #파일을 닫고 자원을 반납