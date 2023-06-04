from datetime import datetime
from datetime import timedelta
from _thread import *
import DB
import socket
import pickle
import struct
from setSocket import *

# HOST = '192.168.202.42' #한서대 와이파이
# PORT = 3650

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))

class Mobility:
    def __init__(self, num):
        self.mobility_n = num
        #self.departure = None
        #self.destination = None
        self.comeIn = None
        self.comeOut = None
        self.status = ''
        self.path = []

    def mobility_set_departure(self, departure):
        self.departure = departure

    def mobility_set_destination(self, destination):
        self.destination = destination

    def comeIn_set(self, comeIn):
        self.comeIn = comeIn

    def comeOut_set(self, comeOut):
        self.comeOut = comeOut

    def status_set(self, status):
        self.status = status

    def receive_path(self, path):
        self.path = path

# m1.mobility_set_departure(1) #임의로 시작점 할당, 
# m1.mobility_set_destination(1) #모빌리티가 계산한 도착점 할당 
# m1.comeIn_set(1) #경로를 기준으로 현재 모빌리티가 있는 위치 저장
# m1.comeOut_set(1) #comeIn이랑 같음
# m1.status = '' #임무에 따른 상태 저장 
# m1.path = '' #경로 저장 

# 임무를 수행할 모빌리티 선정 후 노드에 대한 정보 전송 
# def mobility_choice() : #성공 
def mobility_choice(): #도착지 출발지 무조건 추가하기 
    results = DB.m_info()
    for i in results :
        if i[3] == 'idle' :
            return i[0]

# 선정된 모빌리티로부터 받은 정보를 할당 / 데이터가 어떻게 넘어오는지 알아야 함
def mobility_set_info(M_name, departure, destination) : 
    # 정보가 넘어오면 M_info에 시작, 도착, 상태 변경 
    # 3차원 배열로 넘어올 시 time와 2차원 배열로 변경한 후 가중치 반영 
    if M_name == 'm1' :
        M_name = 'm1'
        m1.mobility_set_departure(departure)
        m1.mobility_set_destination(destination)
    elif M_name == 'm2' :
        M_name = 'm2'
        m2.mobility_set_departure(departure)
        m2.mobility_set_destination(destination)
    elif M_name == 'm3' :
        M_name = 'm3'
        m3.mobility_set_departure(departure)
        m3.mobility_set_destination(destination)
    else :
        print('mobility_set_info error')
    DB.m_info_assignment(M_name, departure, destination)
    
def path_apply(M_name, path) :
    if M_name == 'm1' :
        m1.receive_path(path)
    elif M_name == 'm2' :
        m2.receive_path(path)
    elif M_name == 'm3' :
        m3.receive_path(path)
    else :
        print("경로 설정에 오류 발생")

# 3차원 배열을 2차원으로 변경하는 함수 
def change_arr_3to2(old_arr) : #성공 
    rows = len(old_arr)
    column = len(old_arr[0])
    depth = len(old_arr[0][0])
    
    index = column*depth

    new_arr = [[0 for _ in range(index)] for _ in range(rows)]
    print(new_arr)
    for row in range(rows):
        rr = 0
        for col in range(column):
            for d in range(depth):
                new_arr[row][rr] = old_arr[row][col][d]
                rr += 1
    return new_arr

# 가중치 반영 // 수정이 필요할 수도 
def node_weight_apply(node_weight) :
    for i in node_weight :
        DB.node_info_apply_weight(opTime, node_weight) # 배열에 시간이 넘어오면 DB쪽 함수도 바꿔야함 
        
# comein comeout을 송신 
def comeIn_comeOut(M_name, path) :
    #path에서 단위시간에 맞게 전송 
    try :
        for i in range(len(path)) : 
            comeIn = path[i]
            comeOut = path[i+1]
            if M_name == m1 :
                m1.comeIn_set(comeIn)
                m1.comeOut_set(comeOut)
            elif M_name == m2 :
                m2.comeIn_set(comeIn)
                m2.comeOut_set(comeOut)
            elif M_name == m3 :
                m3.comeIn_set(comeIn)
                m3.comeOut_set(comeOut)
            else :
                print("INOUT 설정에 오류 발생")
            #전송문 
            # 모빌리티로부터 지남 신호(시작 신호)를 대기
            #신호를 받으면 다시 for 진행 
            #???? 통신 시간이 굉장히 까다로운....
            #???? comein이 지나서 새로운 comein comeout을 할당 모빌리티쪽은 comeout만 보고 가는 것인가?? 
    except :
        comeOut = path[i]
        #전송문 

#임무 완료 시
def misson_complete(M_name) :
    DB.m_info_finish(M_name)
    DB.del_path(M_name)

m1 = Mobility(1) # 데이터베이스에서 사용가능한 모빌리티 할당 
m2 = Mobility(2)
m3 = Mobility(3)

opTime  =  datetime.today().strftime("%Y%m%d%H%M%S") #시작 시간 / 송신 / 노테이블
gcsTime =  timedelta(seconds=2) #단위 시간 / 송신 / 노테이블
node_n = [] #노드 / 송신 / T1
weight_n =  []  #가중치 /송신 / T1 
        
def convert_dict_values_to_list(dictionary):
    values_list = list(dictionary.values())
    return values_list



# start_new_thread(gcsData, (client_socket,))
# print('>> Connect server')  


# while True:
#     message = input('')
#     if message == 'quit':
#         close_data = message
#         break

    
#     start = int(input("시작점 : "))
#     curr = int(input("도착점 : "))
#     ## 출발지 도착치 송신
#     send_Int(start, curr)
#     print('모빌리티를 선정합니다.')
#     M_choice = mobility_choice(start, curr)

#     path_data = client_socket.recv(4096)
#     depath = pickle.loads(path_data)
#     path = depath
#     print(path)

#     # choice_M = mobility_choice(dep, des) #모빌리티 선정 
#     # mobility_set_info(choice_M, dep, des) # 시,도,상 할당 
#     # path_apply(choice_M, path) #main에서 받은 path를 여기 함수에서 사용

#     client_socket.send(message.encode())
# client_socket.close()

#     #모빌리티가 path 및 action_cal 정보 수신까지 대기
#     #path랑 action 변수에 넣어주고 
    # on_path(choice_M, path) #pathExtractlor로 받은 경로 할당 
    
#     # action_cal을 mobilitytion_cal로 3차원 배열로 변경
    
#     new_arr = change_arr_3to2(old_arr) # 가중치 배열 체인지
    
#     node_weight_apply(new_arr) # 가중치 할당 
    
#     while(True) :
#         # 수신문 
#         if True == comeIn_comeOut(M_name, path_time) :
#             break
        
#     misson_complete(M_name)
#     break

