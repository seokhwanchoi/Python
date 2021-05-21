# 소켓을 사용하기 위해서는 socket을 import해야 한다.
import socket, json

from numpy.f2py.f2py2e import main

 
# 로컬은 127.0.0.1의 ip로 접속한다.
        
# port는 위 서버에서 설정한 9999로 접속을 한다.
class RemoteCameraApi:
    
    def __init__(self, HOST, PORT):
        # socket open
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

    def run_one_image(self, jsonfile):

        # Tx data
        #print(jsonfile)
        #print(type(json.dumps(jsonfile)))
        self.client_socket.sendall(json.dumps(jsonfile).encode('UTF-8'))
        #dumps : dict -> str
        
        # Rx echo
        data = self.client_socket.recv(4096)
       
        print('Received from : ', data)
            
    def close(self):
        self.client_socket.close()


if __name__=='__main__':
    rca=RemoteCameraApi('192.168.2.91',9999)  #127.0.0.1
    jsonex ={
        'command' : 'save', 
        'contents': 'json_lecture.jpg'
        
    }
    print('json 타입 : ', type(jsonex))
    rca.run_one_image(jsonex)
    rca.close()



 
# # 10번의 루프로 send receive를 한다.
# for i in range(1,10):
#   # 메시지는 hello로 보낸다.
#   msg = 'acquistion_1_{}.jpg'.format(i)
#   # 메시지를 바이너리(byte)형식으로 변환한다.
 
