import socket
import sys
import multiprocessing


def handle_client(cs,addr):

    while True:
        bs=cs.recv(100)
        print(bs)
        if not bs:
            break
        for c in bs:
            cs.send(b'*')
    print('disconnected',addr)


ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
ss.bind(("",9999))
ss.listen(5)

while True:
    cs,addr=ss.accept()
    print('connected',addr)
    process=multiprocessing.Process(target=handle_client,args=(cs,addr))
    process.daemon=True
    process.start()
    cs.close()
