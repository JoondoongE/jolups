from gcs import *
from setSocket import *
import DB
import subprocess
import sys
import threading
import locale
import socket


# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))

#제한 시간을 가진 Input 기능 코드
class Local:
    # check if timeout occurred
    _timeout_occurred = False

    def on_timeout(self, process):
        self._timeout_occurred = True
        process.kill()
        # clear stdin buffer (for Linux)
        try:
            import termios
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except ImportError:
            # Windows, just exit
            pass

    def input_timer_main(self, prompt_in, timeout_sec_in):
        # print with no new line
        print(prompt_in, end="")
        sys.stdout.flush()

        # new python input process create
        cmd = [sys.executable, '-c', 'print(input())']
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            timer_proc = threading.Timer(timeout_sec_in, self.on_timeout, [proc])
            try:
                # timer set
                timer_proc.start()
                stdout, stderr = proc.communicate()

                # get stdout and trim new line character
                result = stdout.decode(locale.getpreferredencoding()).strip("\r\n")
            finally:
                # timeout clear
                timer_proc.cancel()

        # timeout check
        if self._timeout_occurred or not result:
            # move the cursor to the next line
            print("")
            return None  # Return None when timeout occurs or no input is provided
        return result
    
def input_timer(prompt, timeout_sec):
    t = Local()
    return t.input_timer_main(prompt, timeout_sec)

#Program start
processCount = 0
mobilityCount = 0

print('지씨에스메인 시작!')

while True:
    #출발지, 목적지 입력 제한시간 내 입력. 만약 시간 내에 입력 되지 않으면 사이클 돌아감. 여기서는 1초로 지점
    start = 0
    curr = 0

    try:
        start = None
        curr = None
        a = input_timer("* start: ", 2)
        if a is None:
            print("Timeout occurred!")
        else:
            start = int(a)

        a = input_timer("* curr: ", 2)
        if a is None:
            print("Timeout occurred!")
        else:
            curr = int(a)

        print("start:", start)
        print("curr:", curr)

    except TimeoutError as e:
        print("Timeout...")
        print("start:", start)
        print("curr:", curr)
        pass

    print("done")
    

    if (start != None and curr != None):
        if(start == 0 or curr == 0):
            print("Wrong Node")
        else:
            #모빌리티 생성
            mobilityCount = mobilityCount + 1
            print('mobilityCount: ', mobilityCount)
            
            #모빌리티에게 출발지 목적지 송신
            send_Int(start, curr)
            print('모빌리티를 선정합니다.')
            choice_M = mobility_choice()
            print('선정된 모빌리티는 ', choice_M, ' 입니다.')

            #모빌리티에게 DB에 저장된 현재 가중치 송신
            resul = DB.systemOn_node_info()
            send_List(resul) #노드 상태 정보 송신
            mobility_set_info(choice_M, start, curr) # 시,도,상 할당 
            # path_apply(choice_M, path) #main에서 받은 path를 여기 함수에서 사용


            #수신 대기 중 만약 path, action 이 수신 된다면 아래 코드 계속
            #가중치 계산 함수 실행

    #else:
        #comeIn, comeOut이 들어오면 어떤 모빌리티에서 받았는지 파악 후 그 모빌리티의 위치 DB에 갱신

    #if (): 
        #모빌리티에게서 행동 끝 신호를 받는 다면 실행
        #가중치 감소 함수 실행 (weight, 모빌리티 번호, 경로) 를 이용하여 그 모빌리티의 경로를 불러오고 그 경로에 맞게 가중치 감소하도록 수정하기
        #생성된 모빌리티 객체 삭제
    
    #else:
        #그냥 넘어가서 반복문 돌기

    processCount = processCount + 1
    print('processCount: ', processCount)
