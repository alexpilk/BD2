import tkinter as tk
from tkinter import messagebox
from app.api import api
from .klient_home import KlientPage
from .pracownik_home import PracownikPage
from .base import BaseFrame
from .register_form import RegisterPage


class LoginPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10, padx=10)

        self.username_input = tk.Entry(self)
        self.password_input = tk.Entry(self, show="*")
        self.login_button = tk.Button(self, text="Login", command=self.log_in)
        self.register_button = tk.Button(self, text="Register", command=self.register)

        self.username_input.pack()
        self.password_input.pack()
        self.login_button.pack()
        self.register_button.pack()

    def log_in(self):
        username = self.username_input.get()
        password = self.password_input.get()
        if not username or not password:
            messagebox.showinfo('Error', 'Wprowadź dane logowania. Po coś są te pola')
            return
        login_data = api.get('DaneLogowania', filters={
            'login': username,
            'haslo': password
        })
        if not login_data:
            messagebox.showinfo('Error', 'Podano błędne dane logowania. Z kim ja pracuję... -_-')
            return
        klient = api.get('Klient', filters={
            'dane_logowania.login': username
        })
        if klient:
            self.controller.set_user(klient[0])
            self.controller.show_frame(KlientPage)
            return
        pracownik = api.get('Pracownik', filters={
            'dane_logowania.login': username
        })
        if pracownik:
            self.controller.set_user(pracownik[0])
            self.controller.show_frame(PracownikPage)
            return

    def register(self):
        self.controller.show_frame(RegisterPage)
        return