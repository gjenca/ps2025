import socket
import sys
import os
import signal


ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
ss.bind(("",9999))
ss.listen(5)
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
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



