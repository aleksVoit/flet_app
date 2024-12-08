import flet as ft
import sqlite3


def main(page: ft.Page):
    page.title = 'Basic App'
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 350
    page.window.height = 400
    page.window.resizable = False

    users_list = ft.ListView(spacing=10, padding=20)

    def register(e):
        db = sqlite3.connect('users.db')

        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        login TEXT,
        pass TEXT
        )
        """)
        cur.execute(f"""INSERT INTO users VALUES(NULL, '{user_login.value}', '{user_pass.value}')""")
        db.commit()
        db.close()

        user_login.value = ''
        user_pass.value = ''
        btn_reg.text = 'User added'
        page.update()

    def auth_user(e):
        db = sqlite3.connect('users.db')

        cur = db.cursor()

        cur.execute(f"""SELECT * FROM users WHERE login = '{user_login.value}' AND pass = '{user_pass.value}'""")
        if cur.fetchone() is not None:
            user_login.value = ''
            user_pass.value = ''
            btn_auth.text = 'User authorised'
            if len(page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(ft.NavigationBarDestination(
                    icon=ft.Icons.BOOK,
                    label='Cabinet',
                    selected_icon=ft.Icons.BOOKMARK)
                )
            page.update()
        else:
            snack_bar = ft.SnackBar(ft.Text('Wrong login or password'))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

        db.close()

    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True
        page.update()

    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()
        match index:
            case 0: page.add(panel_register)
            case 1: page.add(panel_auth)
            case 2:
                page.add(panel_cabinet)
                users_list.controls.clear()
                # for i in range(5):
                #     users_list.controls.append(ft.Row([
                #         ft.Text(f'User {i}'),
                #         ft.Icon(ft.Icons.VERIFIED_USER_ROUNDED),
                #     ]))
                db = sqlite3.connect('users.db')

                cur = db.cursor()
                cur.execute("""SELECT * FROM users""")
                res = cur.fetchall()
                if res is not None:
                    for user in res:
                        users_list.controls.append(ft.Row([
                            ft.Text(f'Username: {user[1]}'),
                            ft.Icon(ft.Icons.VERIFIED_USER_ROUNDED)
                        ]))
                db.close()
        page.update()

    user_login = ft.TextField(label='Log in', width=200, on_change=validate)
    user_pass = ft.TextField(label='Password', password=True, width=200, on_change=validate)
    btn_reg = ft.OutlinedButton(text='Add', width=200, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton(text='Log in', width=200, on_click=auth_user, disabled=True)

    panel_register = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Registration'),
                    user_login,
                    user_pass,
                    btn_reg
                ]

            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_auth = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Authorization'),
                    user_login,
                    user_pass,
                    btn_auth
                ]

            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_cabinet = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Personal cabinet'),
                    users_list,

                ]
            )
        ], alignment=ft.MainAxisAlignment.CENTER
    )

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.VERIFIED_USER, label='Registry'),
            ft.NavigationBarDestination(icon=ft.Icons.VERIFIED_USER_OUTLINED, label='Authorization'),
        ],
        on_change=navigate
    )

    page.add(panel_auth)


ft.app(target=main)
