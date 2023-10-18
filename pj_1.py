from time import sleep
from typing import Tuple
from threading import Thread
import socket
from config import *

class NetworkSocket:
    
    def __init__(self) -> None:
        self.tcp_socket = None
        self.udp_socket = None
        self.target_tcp_addr = None
        self.target_udp_addr = None

    @staticmethod
    def tcp_server_socket(host: str, port: int) -> socket.socket:
        # TCP server socket 생성
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host,port))
        server_socket.listen(10)
        
        return server_socket


    @staticmethod
    def tcp_server_connect(server_socket: socket.socket) -> Tuple[socket.socket, any]:
        # Server_socket을 통해 client와의 connection 생성 
        # 생성된 connection socket(conn)과 client의 address(tcp_client_addr) 반환 
        conn, addr = server_socket.accept()
        print(str(addr),"에서 접속")
        return conn, addr

    @staticmethod
    def tcp_client_socket(host: str, port: int) -> socket.socket:
        # TCP client socket 생성
        # Server에 connection을 요청하고, server와 client 간 tcp socket(tcp_client_socket) 반환
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"host: {host}, port : {port}")
        return client_socket

    @staticmethod
    def udp_server_socket(host: str, port: int) -> socket.socket:
        # UDP server socket 생성
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((host,port))
        
        return server_socket

    @staticmethod
    def udp_server_connect(udp_server_socket: socket.socket):
        # udp_client_socket 함수가 전송한 packet으로부터 client의 udp address(udp_client_addr) 반환 
        data, addr = udp_server_socket.recvfrom(BUFFER_SIZE)
        
        return addr

    @staticmethod
    def udp_client_socket(host: str, port: int) -> socket.socket:
        # UDP client socket 생성
        # UDP 통신으로 server에 packet을 전송하고 udp client socket(udp_client_socket) 반환
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(b"TEST", (host, port))
        
        return client_socket
        

    def tcp_send(self, data: bytes) -> None:
        # TCP socket(tcp_socket)을 통해 입력 받은 data 전송
        self.tcp_socket.sendall(data)
        
        
        
    def udp_send(self, data: bytes) -> None:
        # UDP socket(udp_socket)를 통해 상대방의 udp 주소(target_udp_addr)로 입력받은 data 전송 
        self.udp_socket.sendto(data, self.target_udp_addr)
        

    def tcp_recv(self) -> bytes:
        # TCP socket(tcp_socket)으로 들어오는 packet의 data 반환  
        data = self.tcp_socket.recv(BUFFER_SIZE)
        
        return data

    def udp_recv(self) -> bytes:
        # UDP socket(udp_socket)으로 들어오는 packet의 data 반환 
        data, _ = self.udp_socket.recvfrom(BUFFER_SIZE)
        return data


    def close(self) -> None:
        try:
            self.tcp_socket.close()
        except socket.error as msg:
            print(f"Unexpected {msg}, {type(msg)}")

        try:
            self.udp_socket.close()

        except socket.error as msg:
            print(f"Unexpected {msg}, {type(msg)}")

    def server_open_func(self, host: str = "", tcp_port: int = DEFAULT_TCP_PORT,
                        udp_port: int = DEFAULT_UDP_PORT) -> int:
        try:
            server_socket = self.tcp_server_socket(host, tcp_port)
            self.tcp_socket, self.target_tcp_addr = self.tcp_server_connect(server_socket)
            self.udp_socket = self.udp_server_socket(host, udp_port)
            self.tcp_send("ack".encode(ENCODING))
            self.target_udp_addr = self.udp_server_connect(self.udp_socket)
            return 0

        except socket.error as msg:
            print(f"Unexpected {msg}, {type(msg)}")
            return -1

    def client_connect_func(self, host: str = "", tcp_port: int = DEFAULT_TCP_PORT,
                            udp_port: int = DEFAULT_UDP_PORT) -> int:
        try:
            self.target_tcp_addr = (host, tcp_port)
            self.target_udp_addr = (host, udp_port)
            self.tcp_socket = self.tcp_client_socket(host, tcp_port)
            _ = self.tcp_recv()  # recv ack
            self.udp_socket = self.udp_client_socket(*self.target_udp_addr)
            return 0

        except socket.error as msg:
            print(f"Unexpected {msg}, {type(msg)}")
            return -1
