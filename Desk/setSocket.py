import socket
import pickle
from _thread import *
import struct
from gcs import *
import DB
from ignore import HOST 
from ignore import PORT



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#recieve message from server

def recv_List():


    list = client_socket.recv(4096)
    recdata_list = pickle.loads(list)
    print("Receive List : ", recdata_list)
    return recdata_list

# start_new_thread(recv_data, (client_socket,))
# print('>> Connect server')

def recv_Int():
    data = client_socket.recv(8)
    daInt = struct.unpack('!ii',data)
    start, curr = daInt

    return start, curr


def send_List(resul):
    results = DB.m_info()
    for i in results :
        if i[3] == 'idle' :
            array = list(resul)
            data = pickle.dumps(array)
            client_socket.sendall(data)
            return f'{i[0]} 모빌리티 선정 및 정보 수신 완료'


def send_Int(start, curr):
    daInt = struct.pack('!ii', start, curr)
    client_socket.sendall(daInt)
    return f'출발지, 도착지 정보 송신 완료'
    # choice_M = mobility_choice(start, curr) #모빌리티 선정
    # return choice_M


# while True:
#     message = input('')
#     if message == 'quit':
#         close_data = message
#         break
    
#     client_socket.send(message.encode())

# client_socket.close()