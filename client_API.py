import socket
# import threading

BUFFER = 1024
# IP = 'localhost'
IP = 'YOUR REMOTE SERVER IP'
PORT = 7777
SERVER_ADDR = (IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 当前用户名
now_username = ''


def receive_messages():
    # 阻止接收消息超时
    client.settimeout(None)
    data, server = client.recvfrom(BUFFER)
    return data.decode()


def login(username, password):
    global now_username
    login_message = f"LOGIN {username} {password}"
    client.sendto(login_message.encode(), SERVER_ADDR)
    # 设置超时时间 以防累计太多消息
    client.settimeout(2)
    try:
        response, add = client.recvfrom(BUFFER)
    except socket.timeout:
        return 'server_down'
    print(response.decode())
    if response.decode() == 'Login successful':
        now_username = username
        return 'ok'
    else:
        return 'error'


def register(username, password):
    registration_message = f"REGISTER {username} {password}"
    client.sendto(registration_message.encode(), SERVER_ADDR)
    # 设置超时时间 以防累计太多消息
    client.settimeout(2)
    try:
        response, add = client.recvfrom(BUFFER)
    except socket.timeout:
        return 'server_down'
    if response.decode() == '[+] 注册成功':
        return 'ok'
    else:
        return 'error'


def list_online_users():
    list_message = f"GET_ONLINE USERS"
    client.sendto(list_message.encode(), SERVER_ADDR)
    response, add = client.recvfrom(BUFFER)
    rev = response.decode()
    return rev


def send_message(message):
    if message == "exit":
        exit_message = f"EXIT {now_username}"
        client.sendto(exit_message.encode(), SERVER_ADDR)
    elif message.startswith("@"):
        try:
            to_address = message.split(" ")[0].replace("@", "")
        except Exception as e:
            print(e)
            return "error"
        private_message = message.split(" ")[1]
        private_message = f"PRIVATE {to_address} {private_message}"
        client.sendto(private_message.encode(), SERVER_ADDR)
    else:
        public_message = f"PUBLIC {message}"
        client.sendto(public_message.encode(), SERVER_ADDR)
