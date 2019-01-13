import tkinter as tk
from tkinter import messagebox
from app.api import api
from .klient_home import KlientPage
from .pracownik_home import PracownikPage


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10, padx=10)
        self.controller = controller

        self.username_input = tk.Entry(self)
        self.password_input = tk.Entry(self, show="*")
        self.login_button = tk.Button(self, text="Login", command=self.log_in)

        self.username_input.pack()
        self.password_input.pack()
        self.login_button.pack()

    def log_in(self):
        username = self.username_input.get()
        password = self.password_input.get()
        if not username or not password:
            messagebox.showinfo('Error', 'Please enter username and password')
            return
        login_data = api.get('DaneLogowania', filters={
            'login': username,
            'haslo': password
        })
        if not login_data:
            messagebox.showinfo('Error', 'Wrong username or password')
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
