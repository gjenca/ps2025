
import sys
import socket
import struct
import os

FNM='Capybara_Hattiesburg_Zoo_(70909b-42)_2560x1600.jpg'

OPCODE_RRQ=1
OPCODE_WRQ=2
OPCODE_DATA=3
OPCODE_ACK=4
OPCODE_ERROR=5

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('127.0.0.1',9999))
while True:
    data,addr=s.recvfrom(1024)
    opcode=struct.unpack('!H',data[:2])[0]
    if opcode!=OPCODE_RRQ:
        print(f'Opcode {opcode} not implemented',file=sys.stderr)
        sys.exit(1)
    filename,mode,ignore=data[2:].split(b'\x00')
    print(opcode)
    print(filename,mode)
    if os.fork()==0:
        opcode_reply=struct.pack('!H',OPCODE_DATA)
        s_r=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        n=0
        with open(FNM,'rb') as f:
            while True:
                print('Reading')
                send_back=f.read(512)
                print('Done')
                n=n+1
                block_num=struct.pack('!H',n)
                reply=opcode_reply+block_num+send_back
                print('Sending reply',n)
                s_r.sendto(reply,addr)
                data,addr=s_r.recvfrom(1024)
                opcode=struct.unpack('!H',data[:2])[0]
                block_num=struct.unpack('!H',data[2:4])[0]
                print(opcode,block_num)
                if not send_back:
                    print('Finito')
                    break
#print(data,addr)
