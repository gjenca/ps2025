import socket
import sys
import os

ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(("",9998))
ss.listen(5)
while True:
    cs,addr=ss.accept()
    print('connected',addr)
    if not os.fork():
        while True:
            bs=cs.recv(100)
            print(bs)
            if not bs:
                break
            for c in bs:
                cs.send(b'*')
        print('disconnected',addr)
        sys.exit(0)
    else:
        cs.close()



