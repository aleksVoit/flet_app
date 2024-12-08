import flet as ft
import os
import dotenv
import requests

env = dotenv.load_dotenv()


def main(page: ft.Page):
    page.title = "Weather App"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_data = ft.TextField(label='Enter the city', width=400)
    weather_data = ft.Text('')

    def change_theme(e):
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()

    def get_info(e):
        if len(user_data.value) < 2:
            return
        api_key = os.getenv('API_WEATHER')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={user_data.value}&appid={api_key}&units=metric'
        res = requests.get(url).json()
        temp = res['main']['temp']
        weather_data.value = 'Temperature ' + str(temp)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.Icons.SUNNY, on_click=change_theme),
                ft.Text('The weather')

            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([weather_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton(text='Get INFO', on_click=get_info)], alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main)
