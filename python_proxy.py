# -*- coding: utf-8 -*-
import socket, threading
from struct import unpack
from pymysql import Connection

HOST = '0.0.0.0'
PORT = 3306

DEST_HOST = '192.168.0.7'
DEST_PORT = 3306

dataBuffer = bytes()
headerSize = 4

def send(sender, reciver):
    while True:
        try:
            data = sender.recv(1024)
        except:
            break
            print "recv error"
        try:
            reciver.sendall(data)
        except:
            break
            print "send error"
    sender.close()
    reciver.close()

def proxy(client):
    dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest_socket.connect((DEST_HOST, DEST_PORT))
    threading.Thread(target=send, args=(client, dest_socket)).start()
    threading.Thread(target=send, args=(dest_socket, client)).start()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print 'server is listen on 0.0.0.0:3306'

    while True:
        conn, addr = server_socket.accept()
        print conn, addr
        threading.Thread(target=proxy, args=(conn, )).start()

if __name__ == '__main__':
    start_server()
