import tkinter as tk
from tkinter import messagebox
from app.api import api
from .base import BaseFrame


class RegisterPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.username_label = tk.Label(self)
        self.username_input = tk.Entry(self)
        self.password_label = tk.Label(self)
        self.password_input = tk.Entry(self, show="*")
        self.password_label2 = tk.Label(self)
        self.password_input2 = tk.Entry(self, show="*")
        self.register_button = tk.Button(self, text="Zarejestruj się", command=self.register)

        self.username_label.pack()
        self.username_input.pack()
        self.password_label.pack()
        self.password_input.pack()
        self.password_label2.pack()
        self.password_input2.pack()
        self.register_button.pack()

    def tkraise(self, *args, **kwargs):
        self.label.config(text=f"Witamy na stronie rejestracji! Podaj dane:")
        self.username_label.config(text="Nazwa użytkownika:")
        self.password_label.config(text="Hasło:")
        self.password_label2.config(text="Powtórz hasło:")
        super().tkraise()

    def register(self):
        username = self.username_input.get()
        password1 = self.password_input.get()
        password2 = self.password_input2.get()

        if not username or not password1:
            messagebox.showinfo('Error', 'Podaj dane do rejestracji, niedoedukowany dzbanie...')
            return

        if password1 != password2:
            messagebox.showinfo('Error', 'Podano dwa różne hasła! Ogarnij sie.')
            return

        login_data = api.get('DaneLogowania', filters={
            'login': username
        })

        if login_data:
            self.label.config(text=f"Witamy na stronie rejestracji! Podaj dane:")
            messagebox.showinfo('Error', 'Ten login jest zajęty! Wymyśl inny.')
            return

        messagebox.showinfo('Error not found', 'Chyba jest dobrze, można robić klienta.')

        return
