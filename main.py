import pyrebase
import flet
from flet import *
import datetime
from functools import partial
import webbrowser

# Firebase Configuration
config = {
    "apiKey": "AIzaSyDbun2SoIBaLQ_oedCVVmuQqYFvxCjpnhw",
    "authDomain": "flet-login-baea4.firebaseapp.com",
    "projectId": "flet-login-baea4",
    "storageBucket": "flet-login-baea4.appspot.com",
    "messagingSenderId": "391263041208",
    "appId": "1:391263041208:web:6bd04d49608f5eda03264d",
    "measurementId": "G-0W2JR5MB1M",
    "databaseURL": "",
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# User Widget Class
class UserWidget(UserControl):
    def __init__(self, title, sub_title, btn_name, func, switch_func=None, switch_label=None):
        self.title = title
        self.sub_title = sub_title
        self.btn_name = btn_name
        self.func = func
        self.switch_func = switch_func
        self.switch_label = switch_label
        super().__init__()

    def InputTextField(self, text, hide):
        return Container(
            alignment=alignment.center,
            content=TextField(
                height=48,
                width=255,
                bgcolor="#ffffff",  # Lighter background for text input
                text_size=12,
                color="#333333",  # Darker text color for readability
                hint_text=text,
                filled=True,
                cursor_color="#5E81F4",  # Highlighted cursor color
                hint_style=TextStyle(size=11, color="#888888"),  # Lighter hint text color
                password=hide,
            ),
        )

    def SocialSignInOption(self, path, name, redirect_url):
        return Container(
            content=ElevatedButton(
                content=Row(
                    alignment='center',
                    spacing=4,
                    controls=[
                        Image(src=path, width=30, height=30),
                        Text(name, color="#333333", size=10, weight="bold"),
                    ],
                ),
                style=ButtonStyle(
                    shape={"": RoundedRectangleBorder(radius=8)},
                    bgcolor={"": "#F0F4FC"},  # Softer background color for social buttons
                ),
                height=48,
                width=255,
                on_click=lambda e: webbrowser.open(redirect_url)  # Opens the external URL for social login
            )
        )

    def build(self):
        self._title = Container(
            alignment=alignment.center,
            content=Text(self.title, size=15, text_align="center", weight="bold", color="#2C3E50"),  # Darker title text
        )

        self._sub_title = Container(
            alignment=alignment.center,
            content=Text(self.sub_title, size=10, text_align="center", color="#7F8C8D"),  # Lighter subtitle text color
        )

        self._sign_in = Container(
            content=ElevatedButton(
                on_click=partial(self.func),
                content=Text(self.btn_name, size=11, weight="bold"),
                style=ButtonStyle(
                    shape={"": RoundedRectangleBorder(radius=8)},
                    color={"": "white"},
                    bgcolor={"": "#5E81F4"},  # Blue background for primary button
                ),
                height=48,
                width=255,
            )
        )

        self._switch_button = Container(
            content=ElevatedButton(
                on_click=self.switch_func,
                content=Text(self.switch_label, size=10, weight="bold"),
                style=ButtonStyle(
                    shape={"": RoundedRectangleBorder(radius=8)},
                    bgcolor={"": "#3498DB"},  # Blue background for navigation button
                    color={"": "white"},  # White text for contrast
                ),
                height=40,
                width=255,
            )
        ) if self.switch_func else None

        return Column(
            horizontal_alignment="center",
            controls=[
                Container(padding=10),
                self._title,
                self._sub_title,
                Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("Email", False),
                        self.InputTextField("Password", True),
                    ],
                ),
                Container(padding=5),
                self._sign_in,
                Container(padding=5),
                Column(
                    horizontal_alignment="center",
                    spacing=10,
                    controls=[
                        Container(
                            content=Text("Or continue with", size=10, color="#7F8C8D"),  # Lighter text for the divider
                        ),
                        # Update the social sign-in options with the URLs to Google and Facebook login pages
                        self.SocialSignInOption(
                            "./assets/facebook.png",
                            "Sign In with Facebook",
                            "https://www.facebook.com/v12.0/dialog/oauth?client_id=YOUR_FB_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI"
                        ),
                        self.SocialSignInOption(
                            "./assets/google.png",
                            "Sign In with Google",
                            "https://accounts.google.com/o/oauth2/v2/auth?client_id=YOUR_GOOGLE_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&scope=openid profile email"
                        ),
                    ],
                ),
                Container(padding=5),
                self._switch_button,
            ],
        )

def main(page: Page):
    page.title = "Flet app with Firebase"
    page.bgcolor = "#ECF0F1",  # Light background color for the page
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def _main_column():
        return Container(
            width=280,
            height=600,
            bgcolor="#ffffff",  # White background for the main container
            padding=12,
            border_radius=25,
            content=Column(spacing=20, horizontal_alignment="center"),
        )

    def _register_user(e):
        try:
            auth.create_user_with_email_and_password(
                _register_.controls[0].controls[3].controls[0].content.value,
                _register_.controls[0].controls[3].controls[1].content.value,
            )
            print("Registration OK!")
        except Exception as e:
            print(e)

    def _sign_in(e):
        try:
            user = auth.sign_in_with_email_and_password(
                _sign_in_.controls[0].controls[3].controls[0].content.value,
                _sign_in_.controls[0].controls[3].controls[1].content.value,
            )
            info = auth.get_account_info(user["idToken"])
            data = ["createdAt", "lastLoginAt"]
            for key in info:
                if key == "users":
                    for item in data:
                        print(
                            item
                            + " "
                            + datetime.datetime.fromtimestamp(
                                int(info[key][0][item]) / 1000
                            ).strftime("%D - %H:%M %p")
                        )
        except:
            print("Wrong email and password")

    # Navigation between forms
    def go_to_sign_in(e):
        page.clean()
        page.add(_sign_in_main)
        page.update()

    def go_to_register(e):
        page.clean()
        page.add(_reg_main)
        page.update()

    # Sign-In Widget
    _sign_in_ = UserWidget(
        "Welcome Back!",
        "Enter Your Account details",
        "Sign In",
        _sign_in,
        switch_func=go_to_register,
        switch_label="Go to Register",
    )

    _sign_in_main = _main_column()
    _sign_in_main.content.controls.append(Container(padding=15))
    _sign_in_main.content.controls.append(_sign_in_)

    # Registration Widget
    _register_ = UserWidget(
        "Registration",
        "Register with your email and password",
        "Register",
        _register_user,
        switch_func=go_to_sign_in,
        switch_label="Go to Sign In",
    )

    _reg_main = _main_column()
    _reg_main.content.controls.append(Container(padding=15))
    _reg_main.content.controls.append(_register_)

    # Start with Sign-In Page
    page.add(_sign_in_main)


if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")
