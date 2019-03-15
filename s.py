# -*- coding: utf-8 -*-
import socket,time,threading,json

def headers(data):        #解析数据包
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
    print "发送ping到"+ip

def recv_ping(socket,addr):  #接收客户端的ping
    if addr not in nodes:
        nodes.append(addr)           #添加时间戳
        alive.append([addr,time.time()])
        print("add_new node") 
    send_pong(socket,addr)

def send_pong(socket,addr):
    msg = "Content-Type:PONG\r\n"
    msg += "ip:"+addr[0]+"\r\n"
    msg += "port:"+str(addr[1])+"\r\n"
    msg += "msg:I`m fine!\r\n\r\n" #消息
    socket.sendto(msg.encode("utf-8"),addr)    #回复Pong
    print "回应ping"
    print addr


def get_nodes(socket,addr):  #ask to server
    request = "Content-Type:FIND_NODE\r\n"
    request += "msg:Are you OK!\r\n\r\n" #消息
    print"请求节点"
    print request
    socket.sendto(request.encode("utf-8"),addr)

def nodes_back(socket,addr):    #服务端返回节点列表
    response = "Content-Type:RESPONSE_NODE\r\n"
    str = json.dumps(nodes)
    response += "nodes:"+str+"\r\n\r\n"
    print("返回节点列表")
    socket.sendto(response,addr)

def append_node(addr):
    if addr not in nodes:
        send_pong(socket.socket(socket.AF_INET,socket.SOCK_DGRAM),addr)
        for n in nodes:
            if n[0] == addr[0]:
                nodes.pop(nodes.index(n))  #清除旧的addr
                nodes.append(addr)
                alive.append([addr,time.time()])
                print("add_new node") 
    else:
        for a in alive:
            if a[0] == addr:
                a[1] = time.time()   #更新最后链接时间
                break;

def recv(receive,header,addr):
    header = headers(header)
    if header["Content-Type"] == "PING":    #收到PING数据
        recv_ping(receive,addr)
    if header["Content-Type"] == "FIND_NODE":
        nodes_back(receive,addr)
    if header["Content-Type"] == "HEART":
        print "heart from"
        append_node(addr)
        print addr
        pass
def refrush_nodes(socket):
    while True:
        if len(nodes) > 0:
            print "开始刷新列表"
            for a in alive:
                now = time.time()
                if now - a[1] > 5.0:
                    print "去掉"+a[0][0]
                    nodes.pop(nodes.index(a[0]))  #去掉超过5s未连接的客户机
                    alive.pop(alive.index(a))
            for n in nodes:
                print "刷新列表"
                nodes_back(socket,n)
            time.sleep(5)





nodes = []
alive = []
if __name__ == "__main__":
    addr = ('0.0.0.0',20006)
    receive = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    receive.bind(addr)

    print 'Waiting for connection...'
    t1 = threading.Thread(target=refrush_nodes, args=(receive,))
    t1.start()
    while True:
        # 接受一个新连接:
        header,address = receive.recvfrom(2048)
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=recv, args=(receive,header,address))
        t.start()
        
    

    #receive.close()
