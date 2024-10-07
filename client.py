import socket
import threading

BUFFER = 1024
# IP = 'localhost'
IP = 'YOUR REMOTE SERVER IP'
POST = 7777
SERVER_ADDR = (IP, POST)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def receive_messages():
    while True:
        data, server = client.recvfrom(1024)
        print(data.decode())


def main():
    while True:
        choice = input("请选择功能:\n1. 注册\n2. 登录\n3. 退出\n输入你的选择: ")
        if choice == "1":
            username = input("[*] 输入用户名: ")
            password = input("[*] 输入密码: ")
            registration_message = f"REGISTER {username} {password}"
            client.sendto(registration_message.encode(), SERVER_ADDR)
            response, add = client.recvfrom(BUFFER)
            print(response.decode())
        elif choice == "2":
            username = input("[*] 输入用户名: ")
            password = input("[*] 输入密码: ")
            login_message = f"LOGIN {username} {password}"
            client.sendto(login_message.encode(), SERVER_ADDR)
            response, add = client.recvfrom(1024)
            if response.decode() == "Login successful":
                # print(f"[+] 欢迎 {username} 加入聊天室")
                rev, add = client.recvfrom(1024)
                online_users = list(rev.decode().replace("[", "").replace("]", "").replace("'", "").split(", "))
                print("[*] 当前在线用户: ", end='')
                for user in online_users:
                    print(user, end=' ')
                break
            else:
                print(response.decode())
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("[-] 选项错误，请重新输入")

    # 开启接收消息线程
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    # 发送消息
    while True:
        message = input()
        client.sendto(message.encode(), SERVER_ADDR)
        if message == "exit":
            break
        elif message.startswith("@"):
            to_address = message.split(" ")[0].replace("@", "")
            private_message = message.split(" ")[1]
            private_message = f"PRIVATE {to_address} {private_message}"
            client.sendto(private_message.encode(), SERVER_ADDR)
        else:
            public_message = f"PUBLIC {message}"
            client.sendto(public_message.encode(), SERVER_ADDR)


if __name__ == '__main__':
    main()
