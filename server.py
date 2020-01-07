#!/usr/bin/env python
import json
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65430        # Port to listen on (non-privileged ports are > 1023)

hash_1 = {}
def action_with_hash(message:dict, hash_1:dict, conn):
    action = message["action"]
    if action == "get":
        try:
            datafrHash = hash_1[message["key"]]
            conn.sendall(json.dumps({"status": "Ok", "message": datafrHash}).encode("utf-8"))
        except KeyError:
            conn.sendall(json.dumps({"status": "Bad Request"}).encode("utf-8"))
        except:
            conn.sendall("Internal Server Error".encode("utf-8"))
    elif action == "put":
        try:
            hash_1[message["key"]] = message["message"]
            conn.sendall(json.dumps({"status":"Create"}).encode("utf-8"))
        except:
            conn.sendall("Internal Server Error".encode("utf-8"))

    elif action == "delete":
        try:
            if message["key"]:
                del hash_1[message["key"]]
                conn.sendall(json.dumps({"status":"OK"}).encode("utf-8"))
            else:
                conn.sendall(json.dumps({"status":"Bad request"}).encode("utf-8"))
        except:
            conn.sendall("Internal Server Error".encode("utf-8"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            message = json.loads(data)
            try:
                action_with_hash(message, hash_1, conn)
            except:
                conn.sendall("Bad request".encode("utf-8"))
            my_file = open("var/log/server.log", 'a')
            my_file.write(data.decode('utf-8'))
            conn.sendall("OK:".encode('utf-8')+message["action"].encode("utf-8"))
        my_file.close()
