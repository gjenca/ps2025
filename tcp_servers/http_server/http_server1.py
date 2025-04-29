#!/usr/bin/env python3
import socket
import sys
import multiprocessing
import re
import os.path

STATUS_BAD_REQUEST=(400,'Bad request')
STATUS_OK=(200,'OK')
STATUS_FILE_NOT_FOUND=(404,'File Not Found')

DOCROOT='doc'

MIME_TYPES={
    '.html':'text/html',
    '.jpg':'image/jpeg',
    '.png':'image/png',
    '.txt':'text/plain',
    }

class ConnectionClosed(Exception):

    pass

class ErrorStatus(Exception):

    def __init__(self,status):
        self.status=status

class Response:

    def __init__(self,status_pair,headers=None,content=None):
        
        self.status_n,self.status_desc=status_pair
        self.headers=headers or {}
        if not content:
            self.content=f'''
<html>
<body>
<h1>{self.status_n} {self.status_desc}</h1>
</body>
</html>'''.encode('ascii')
            self.headers['content-length']=f'{len(self.content)}'
        else:
            self.content=content

    def send(self,f):
        
        f.write(f'HTTP/1.1 {self.status_n} {self.status_desc}\r\n'.encode('ascii'))
        for key in self.headers:
            f.write(f'{key}: {self.headers[key]}\r\n'.encode('ascii'))
        f.write('Transfer-Encoding: chunked\r\n'.encode('ascii'))
        f.write('\r\n'.encode('ascii'))
        for chunk_i in range(0,self.content,1000):
            to_send=self.content[chunk_i:chunk_i+1000]
            f.write(hex(len(to_send))[2:].encode('ascii')+'\r\n')
            f.write(to_send)
            f.flush()
        f.write('0\r\n'.encode('ascii')
        f.flush()

class Request:

    def __init__(self,f):

        first_line=f.readline().decode('ascii')
        if not first_line:
            raise ConnectionClosed
        first_line=first_line.strip()
        m=re.match(r'^(\S+) (\S+) (\S+)$',first_line)
        if not m:
            raise ErrorStatus(STATUS_BAD_REQUEST)
        self.method=m.group(1)
        self.url=m.group(2)
        self.version=m.group(3)
        self.headers={}
        while True:
            line=f.readline().decode('ascii')
            if not line:
                raise ConnectionClosed
            line=line.strip()
            if not line:
                break
            m=re.match(r'^(\S+): (.+)$',line)
            if not m:
                raise ErrorStatus(STATUS_BAD_REQUEST)
            # Na velkosti pismen v nazve hlavicky nezalezi
            self.headers[m.group(1).lower()]=m.group(2)

    def __repr__(self):

        return f'Request {self.method=} {self.url=} {self.version=} {self.headers}'
            
            

def handle_client(cs,addr):

    f=cs.makefile('rwb')
    while True:
        try:
            req=Request(f)
            try:
                with open(DOCROOT+req.url,'rb') as ff:
                    content=ff.read()
            except FileNotFoundError:
                raise ErrorStatus(STATUS_FILE_NOT_FOUND)
            headers={}
            ext=os.path.splitext(req.url)[1]
            if ext in MIME_TYPES:
                headers['Content-type']=MIME_TYPES[ext]
            else:
                headers['Content-type']='application/octet-stream'
            resp=Response(STATUS_OK,headers,content)
            resp.send(f)
        except ConnectionClosed:
            break
        except ErrorStatus as es:
            resp=Response(es.status)
            resp.send(f)
    f.close()
    cs.close()



ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
ss.bind(("",9999))
ss.listen(5)

while True:
    cs,addr=ss.accept()
    process=multiprocessing.Process(target=handle_client,args=(cs,addr))
    process.daemon=True
    process.start()
    cs.close()
