# -*- coding: utf-8 -*-
import socket,time,threading,json
nodes = []

def headers(self,data):        #解析数据包
        header_content = data.split('\r\n\r\n', 1)[0].split('\r\n')[0:]
        result = {}
        for line in header_content:
            k, v = line.split(':',1)
            result[k.strip(" ")] = v.strip(" ")
        return result
def send_ping(socket,addr): #send ping
    
    #socket.sendto("ping".encode('UTF_8'),addr)
    request = "Content-Type:PING\r\n"
    request += "msg:Are you OK!\r\n\r\n" #消息
    socket.sendto(request.encode("utf-8"),addr)
    print("send_ping")
    print ("发送ping到"+addr[0])

def recv_ping(socket,addr):  #接收客户端的ping
    while True:
        msg,addr = socket.recvfrom(2048)
        h = headers(msg)
        if(addr not in list_node):
            nodes.append(addr)
            print("add_new node")
        msg = "Content-Type:PONG\r\n"
        msg += "Verif:"+h["Verif"]+"\r\n\r\n" #验证消息
        socket.sendto(msg,addr)
        print(addr,' : ',s)

def recv_pong(socket):   #接收发的pong信息
    while True:
        s,addr = socket.recvfrom(2048)
        if(addr not in list_node):
            nodes.append(addr)
            print("add_new node")
        #time.sleep(2)
def get_nodes(socket,addr):  #ask to server
    request = "Content-Type:FIND_NODE\r\n"
    request += "msg:Are you OK!\r\n" #消息
    print("向请求邻居")
    print (request)
    socket.sendto(request.encode("utf-8"),addr)
def headers(data):        #解析数据包
    print(data)
    data = data.decode("utf-8")
    header_content = data.split('\r\n\r\n', 1)[0].split('\r\n')[0:]
    result = {}
    for line in header_content:
        k, v = line.split(':',1)
        result[k.strip(" ")] = v.strip(" ")
    return result

def nodes_back(socket,addr):    #服务端返回节点列表
    response = "Content-Type:RESPONSE_NODE\r\n"
    
    socket.sendto()
def recv(receive,server_addr):
    while True:
        data,addr = receive.recvfrom(2048)  #收到服务器的回应
        header = headers(data)
        if header["Content-Type"] == "PONG" and addr == server_addr: #收到回应的话每隔几秒发送心跳信息
                t = threading.Thread(target=heart, args=(receive,addr)) 
                t.start()
        if header["Content-Type"] == "RESPONSE_NODE":
            node_list = json.loads(header["nodes"])
            for value in node_list:
                if value not in nodes:
                    nodes.append(tuple(value))
        if header["Content-Type"] == "PONG":
            msg = "Content-Type:NAT\r\n"
            msg += "msg:success\r\n\r\n"
            receive.sendto(msg.encode("utf-8"),addr)
        if header["Content-Type"] == "PING":
            msg = "Content-Type:PONG\r\n"
            msg += "msg:success\r\n\r\n"
            receive.sendto(msg.encode("utf-8"),addr)

def heart(socket,addr):  #发送心跳
    msg = "Content-Type:HEART\r\n"
    msg += "msg:i'm alive!\r\n\r\n"
    while True:
        socket.sendto(msg.encode("utf-8"),addr)
        time.sleep(3)
if __name__ == "__main__":
    addr = ('47.101.137.17',20006)
    receive = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    send_ping(receive, addr)    #say hello与服务器建立连接
    t = threading.Thread(target=recv, args=(receive,addr)) 
    t.start()
    print("获取节点")
    get_nodes(receive, addr)    #获取节点列表
    while True:
        if(len(nodes)>1):
            for i in range(1,len(nodes)):
                print ("发给"+nodes[i]+"客户机")
                send_ping(receive,nodes[i])

    

    t1 = threading.Thread(target=recv_pong, args=(receive)) 
    t1.start()
    print(addr,' : ',data)
    #receive.close()
