
import serial
import threading
import time

#참조 사이트 : https://post.naver.com/viewer/postView.nhn?volumeNo=31037503&memberNo=2534901

line = ''  # 라인 단위로 데이터 가져올 변수
port = '/dev/ttyUSB0' # 시리얼 포트
baud = 115200  # 시리얼 보드레이트(통신속도)

ser = serial.Serial(port, baud, timeout=3)

alivethread = True

# 쓰레드
def readthread(ser):
    global line, alivethread

    print('readthread  시작')
    
    # 쓰레드 종료될때까지 계속 돌림
    while alivethread:
        # 데이터가 있있다면
        for c in ser.read():
            # line 변수에 차곡차곡 추가하여 넣는다.
            line += (chr(c))
            if line.startswith('[') and line.endswith(']'):  # 라인의 끝을 만나면..
                # 데이터 처리 함수로 호출
                print('receive data=' + line)
                # line 변수 초기화
                line = ''

    print('readthread exit')
    ser.close()


def main():

    # 시리얼 읽을 쓰레드 생성
    thread = threading.Thread(target=readthread, args=(ser,))
    thread.start()

    count = 10
    while count > 0:
        strcmd = 'hello'
        for char in strcmd:
            print('send data=' + char)
            ser.write(char.encode())
            time.sleep(0.05)
            count -= 1
        
    # alivethread = False
    


main()