import socket
import sys
import multiprocessing

class ConnectionClosed(Exception):

    pass

class Request:

    def __init__(self,f):
        
        line=f.readline() # vrati bytes
        if not line:
            raise ConnectionClosed
        line=line.decode('utf-8')
        self.method=line.strip()
        self.content=[]
        while True:
            line=f.readline()
            line=line.decode('utf-8')
            if line=='\n':
                break
            self.content.append(line.strip())

class Response:

    def __init__(self,status,content=[]):

        self.status=status
        self.content=content

    def send(self,f):

        f.write(f'{self.status[0]} {self.status[1]}\n'.encode('utf-8'))
        for item in self.content:
            f.write(f'{item}\n'.encode('utf-8'))
        f.write('\n'.encode('utf-8'))
        f.flush()



STATUS_OK=(100,'OK')
STATUS_CONTENT_EMPTY=(201,'Content empty')
STATUS_NOT_A_NUMBER=(202,'Not a number')
STATUS_STACK_TOO_SHORT=(203,'Stack too short')
STATUS_CONTENT_NONEMPTY=(204,'Content nonempty')
STATUS_BAD_REQUEST=(301,'Bad request')

def method_PUSH(req,stack):

    if not req.content:
        return Response(STATUS_CONTENT_EMPTY)
    if not all(s.isdigit() for s in req.content):
        return Response(STATUS_NOT_A_NUMBER)
    for num_s in req.content:
        stack.append(int(num_s))
    return Response(STATUS_OK)

def method_ADD(req,stack):

    if req.content:
        return Response(STATUS_CONTENT_NONEMPTY)
    if len(stack)==0 or len(stack)==1:
        return Response(STATUS_STACK_TOO_SHORT)
    n1=stack.pop()
    n2=stack.pop()
    stack.append(n1+n2)
    return Response(STATUS_OK)

def method_MULTIPLY(req,stack):

    if req.content:
        return Response(STATUS_CONTENT_NONEMPTY)
    if len(stack)==0 or len(stack)==1:
        return Response(STATUS_STACK_TOO_SHORT)
    n1=stack.pop()
    n2=stack.pop()
    stack.append(n1*n2)
    return Response(STATUS_OK)
    

METHODS={
    'PUSH':method_PUSH,
    'ADD':method_ADD,
    'MULTIPLY':method_MULTIPLY,
}

def handle_client(cs,addr):

    stack=[]
    f=cs.makefile('rwb')
    while True:
        try:
            req=Request(f)
        except ConnectionClosed:
            break
        print(f'method:{req.method}')
        print(f'content:{req.content}')
        if req.method in METHODS:
            response=METHODS[req.method](req,stack)
        else:
            response=Response(STATUS_BAD_REQUEST)
            response.send(f)
            break
        response.send(f)
        print(stack)
    print(f'{addr} disconnected')
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
