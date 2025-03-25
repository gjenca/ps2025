import socket
import sys
import multiprocessing


def handle_client(cs,addr):

    f=cs.makefile('rwb')
    while True:
        line=f.readline() # vrati bytes
        if not line:
            break
        line_s=line.decode('utf-8')
        length=len(line_s)
        f.write(f'{length}\n'.encode('utf-8'))
        f.flush()
    f.close()
    cs.close()

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
