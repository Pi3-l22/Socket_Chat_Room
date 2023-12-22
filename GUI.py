import threading

import flet as ft
import client_API as ct


def login_page(page: ft.Page):
    page.title = "多人在线聊天室"
    page.window_bgcolor = ft.colors.TRANSPARENT
    page.bgcolor = "#E1F7FB"
    # page.window_frameless = True
    page.window_width = 500
    page.window_height = 360
    page.window_min_width = 500
    page.window_min_height = 360
    page.window_maximizable = False
    page.window_resizable = False
    page.auto_scroll = True
    page.scroll = "AUTO"
    page.window_center()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.theme.Theme(
        color_scheme_seed='blue', font_family="xiawu")
    page.update()
    # 页面字体
    page.fonts = {
        "xiawu": "font/LXGWWenKaiMonoLite-Bold.ttf",
    }
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_AROUND  # 垂直居中
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 水平居中

    # 登录按钮点击事件
    def btn_login_click(e):
        # 用户名和密码为空
        if username_box.value == '' or password_box.value == '':
            page.dialog = login_empty_dlg
            login_empty_dlg.open = True
            page.update()
            return
        rev = ct.login(username_box.value, password_box.value)
        if rev == 'ok':
            print('登录成功')
            main_page(page)
        elif rev == 'error':
            print('登录失败')
            # 警告弹窗
            page.dialog = login_error_dlg
            login_error_dlg.open = True
            page.update()
        elif rev == 'server_down':
            print('服务器错误！')
            page.dialog = server_error_dlg
            server_error_dlg.open = True
            page.update()


    # 注册按钮点击事件
    def btn_register_click(e):
        rev = ct.register(username_box.value, password_box.value)
        if rev == 'ok':
            print('注册成功')
            # 成功弹窗
            page.dialog = register_success_dlg
            register_success_dlg.open = True
            page.update()
        elif rev == 'error':
            print('注册失败')
            # 警告弹窗
            page.dialog = register_error_dlg
            register_error_dlg.open = True
            page.update()
        elif rev == 'server_down':
            print('服务器错误！')
            page.dialog = server_error_dlg
            server_error_dlg.open = True
            page.update()

    # 错误弹窗
    login_error_dlg = ft.AlertDialog(
        title=ft.Text(
            "用户名或密码错误！\n\n请检查后重新输入！"),
    )
    login_success_dlg = ft.AlertDialog(
        title=ft.Text(
            "登录成功！\n\n欢迎进入聊天室！"),
    )
    register_error_dlg = ft.AlertDialog(
        title=ft.Text(
            "注册失败！\n\n用户名已存在！"),
    )
    register_success_dlg = ft.AlertDialog(
        title=ft.Text(
            "注册成功！\n\n请登录！"),
    )
    login_empty_dlg = ft.AlertDialog(
        title=ft.Text(
            "用户名或密码为空！\n\n请检查后重新输入！")
    )
    server_error_dlg = ft.AlertDialog(
        title=ft.Text(
            "服务器错误！\n\n请稍后尝试！")
    )

    title = ft.Stack(
        [
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "多人在线聊天室",
                        ft.TextStyle(
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            foreground=ft.Paint(
                                color="#439AE6",
                                stroke_width=6,
                                stroke_join=ft.StrokeJoin.ROUND,
                                style=ft.PaintingStyle.STROKE,
                            ),
                        ),
                    ),
                ],
            ),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "多人在线聊天室",
                        ft.TextStyle(
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color="#B0EEF4",
                        ),
                    ),
                ],
            ),
        ]
    )
    # page.add(title)
    password_box = ft.TextField(
        label="密码",
        hint_text="请输入你的密码",
        max_lines=1,
        width=350,
        height=55,
        password=True,
        can_reveal_password=True,
        keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,
        shift_enter=True,
        on_submit=btn_login_click
    )
    username_box = ft.TextField(
        label="用户名",
        hint_text="请输入你的用户名",
        max_lines=1,
        width=350,
        height=55,
        autofocus=True,
        shift_enter=True,
        on_submit=lambda e: password_box.focus(),
    )

    btn_login = ft.ElevatedButton(
        text="登录",
        width=150,
        height=50,
        animate_size=True,
        on_click=btn_login_click,
        icon=ft.icons.LOGIN,
    )
    btn_register = ft.ElevatedButton(
        text="注册",
        width=150,
        height=50,
        animate_size=True,
        on_click=btn_register_click,
        icon=ft.icons.CREATE_OUTLINED,
    )
    # 登录框和按钮
    page.add(ft.Column(
        [
            ft.Row(
                [
                    title
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    # ft.Text("Username:"),
                    username_box
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    # ft.Text("Password:"),
                    password_box
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    btn_login,
                    btn_register
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        # 居中
        spacing=20,
    ))

    page.padding = 20  # 设置内边距
    page.update()


def main_page(page: ft.Page):
    page.clean()
    # page.vertical_alignment = ft.MainAxisAlignment.START  # 垂直居中
    page.horizontal_alignment = "stretch"
    page.window_max_height = 600
    page.window_max_width = 800
    page.window_width = 800
    page.window_height = 600
    # 拦截本机窗口关闭信号 配合关闭窗口默认退出聊天
    page.window_prevent_close = True

    # 接收消息
    def receive_message():
        while True:
            message = ct.receive_messages()
            update_chat(message)

    # 更新聊天框
    def update_chat(message):
        text = ft.Text(value=message)
        chat.controls.append(text)
        page.update()

    # 聊天内容列表
    chat = ft.ListView(
        width=400,
        height=400,
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # 发送消息事件
    def send_message_click(e):
        if new_message.value == ' ' or new_message.value == '':
            return
        ct.send_message(new_message.value)
        new_message.value = ""
        page.update()

    # 发送消息按钮
    btn_send = ft.ElevatedButton(
        text="发送",
        width=120,
        height=50,
        animate_size=True,
        on_click=send_message_click,
        icon=ft.icons.SEND,
    )

    # 输入框
    new_message = ft.TextField(
        label="Message",
        hint_text="输入聊天消息",
        max_lines=1,
        width=500,
        height=60,
        autofocus=True,
        shift_enter=True,
        on_submit=send_message_click,
    )

    # 当前用户头像
    user_avatar = ft.CircleAvatar(
        content=ft.Text(ct.now_username, size=14, weight=ft.FontWeight.BOLD),
        width=60,
        height=60,
    )

    # 添加页面信息
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1),
            border_radius=5,
            padding=10,
            margin=ft.margin.only(bottom=20)
            # expand=True,
        ),
        ft.Row(
            [
                user_avatar,
                new_message,
                btn_send,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
    )
    page.update()

    # 窗口关闭默认退出聊天室
    def close_window(e):
        if e.data == 'close':
            ct.send_message('exit')
            page.window_destroy() # 真正退出窗口

    page.on_window_event = close_window
    # 开启接收消息线程
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()


ft.app(target=login_page, assets_dir="assets")
