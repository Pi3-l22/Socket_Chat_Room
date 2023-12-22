import socket
import threading
# import signal

BUFFER = 1024
IP = '0.0.0.0'
PORT = 7777
SERVER_ADDR = (IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(SERVER_ADDR)

# 记录注册过的用户信息字典
user_dict = {}  # {username: password}
# 记录在线用户信息字典
online_user = {}  # {username: (ip, port)}


def init_users():
    with open('users.txt', 'r') as f:
        for line in f.readlines():
            username = line.split(',')[0]
            password = line.split(',')[1].replace('\n', '')
            user_dict[username] = password
    print(f'[+] 注册用户信息加载成功')


def save_users():
    with open('users.txt', 'w') as f:
        for username in user_dict.keys():
            password = user_dict[username]
            f.write(f'{username},{password}\n')


def list_online_users(address):
    users = []
    for username in online_user.keys():
        users.append(username)
    rev = "[+] 当前在线用户: "
    print(f'{rev} {users}')
    for user in users:
        rev += user + ' '
    server.sendto(rev.encode(), address)


def register(username, password, address):
    if username in user_dict.keys():
        server.sendto("[-] 用户名已存在".encode(), address)
    else:
        user_dict[username] = password
        save_users()
        server.sendto("[+] 注册成功".encode(), address)


def login(username, password, address):
    if username not in user_dict.keys():
        server.sendto("[-] 用户名不存在".encode(), address)
    elif user_dict[username] != password:
        server.sendto("[-] 密码错误".encode(), address)
    else:
        server.sendto("Login successful".encode(), address)
        online_user[username] = address
        # 发送上线通知
        for online in online_user.keys():
            server.sendto(f'\n[+] 欢迎 {username} 加入聊天室'.encode(), online_user[online])
            # 发送在线用户列表
            list_online_users(online_user[online])


def public_chat(message, address):
    from_username = ""
    # 通过address获取username
    for username in online_user.keys():
        if online_user[username] == address:
            from_username = username
            break
    for username in online_user.keys():
        server.sendto(f'[+] {from_username}: {message}'.encode(), online_user[username])


def private_chat(message, to_username, address):
    from_username = ""
    # 通过address获取username
    for username in online_user.keys():
        if online_user[username] == address:
            from_username = username
            break
    if to_username not in online_user.keys():
        server.sendto("[-] 私聊用户不在线".encode(), address)
    else:
        to_address = online_user[to_username]
        server.sendto(f'[@] {from_username}: {message}'.encode(), to_address)
        server.sendto(f'[@] {from_username}: {message}'.encode(), address)


def exit_chat(username, address):
    # 删除在线用户 并发送下线通知
    for user in online_user.keys():
        server.sendto(f'\n[-] {username} 已离开聊天室'.encode(), online_user[user])
    del online_user[username]
    # 发送在线用户列表
    for username in online_user.keys():
        list_online_users(online_user[username])


def menu(data, address):
    command = data.split()[0]
    if command == "REGISTER":
        username = data.split()[1]
        password = data.split()[2]
        register(username, password, address)
    elif command == "LOGIN":
        username = data.split()[1]
        password = data.split()[2]
        login(username, password, address)
    elif command == "PUBLIC":
        message = data.split()[1]
        public_chat(message, address)
    elif command == "PRIVATE":
        to_username = data.split()[1]
        message = data.split()[2]
        private_chat(message, to_username, address)
    elif command == 'GET_ONLINE':
        list_online_users(address)
    elif command == 'EXIT':
        username = data.split()[1]
        exit_chat(username, address)


def exit_server(signum, frame):
    print('\n[-] 服务器已关闭')
    save_users()
    server.close()
    exit()


def main():
    print('[*] 服务器已启动...')
    while True:
        try:
            data, address = server.recvfrom(BUFFER)
            message = data.decode()
            if message == ' ' or message == '' or message == '\n':
                continue
            print(f'[+] 收到来自 {address} 的消息: {message}')
            # 开启线程处理消息
            threading.Thread(target=menu, args=(message, address)).start()
        except KeyboardInterrupt:
            exit_server(0, 0)
        except Exception as e:
            print(f'[-] 服务器异常: {e}')
            continue
        # 按下Ctrl+C退出
        # signal.signal(signal.SIGINT, exit_server)


if __name__ == '__main__':
    init_users()
    main()
