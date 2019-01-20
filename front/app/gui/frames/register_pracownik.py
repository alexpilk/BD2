import tkinter as tk
from tkinter import messagebox
from app.api import api
from .base import BaseFrame
# from .klient_home import KlientPage
from .pracownik_home import PracownikPage


class RegisterPrac(BaseFrame):

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
        self.name_label = tk.Label(self)
        self.name_input = tk.Entry(self)
        self.lastname_label = tk.Label(self)
        self.lastname_input = tk.Entry(self)
        self.email_label = tk.Label(self)
        self.email_input = tk.Entry(self)
        self.money_label = tk.Label(self)
        self.money_input = tk.Entry(self)
        self.address_label = tk.Label(self)
        self.address_input = tk.Entry(self)

        self.descriptions_get = []
        self.descriptions_get = api.get(
            'Stanowisko',
            fields={
                "IdStanowiska": ['id'],
                "NazwaStanowiska": ['nazwa']
            }
        )
        self.elements = []
        for i in range(len(self.descriptions_get)):
            self.elements.append(self.descriptions_get[i]['nazwa'])

        self.stanowisko = tk.StringVar(self)
        self.work_list = tk.OptionMenu(self, self.stanowisko, *self.elements)

        self.register_button = tk.Button(self, text="Dodaj pracownika", command=self.register)
        self.return_button = tk.Button(self, text="Wróć do strony pracownika", command=self.tohome)

        self.register_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')

        self.username_label.pack()
        self.username_input.pack()
        self.password_label.pack()
        self.password_input.pack()
        self.password_label2.pack()
        self.password_input2.pack()
        self.name_label.pack()
        self.name_input.pack()
        self.lastname_label.pack()
        self.lastname_input.pack()
        self.email_label.pack()
        self.email_input.pack()
        self.money_label.pack()
        self.money_input.pack()
        self.address_label.pack()
        self.address_input.pack()
        self.work_list.pack()
        self.register_button.pack()
        self.return_button.pack()

    def tkraise(self, *args, **kwargs):
        self.label.config(text=f"Witamy na stronie rejestracji nowego pracownika! "
                               f"Podaj dane:")
        self.username_label.config(text="Login:")
        self.password_label.config(text="Hasło:")
        self.password_label2.config(text="Powtórz hasło:")
        self.name_label.config(text="Imię:")
        self.lastname_label.config(text="Nazwisko:")
        self.email_label.config(text="Adres email:")
        self.money_label.config(text="Miesięczna pensja:")
        self.address_label.config(text="Adres zamieszkania:")

        self.stanowisko.set("---")

        self.username_input.delete(0, tk.END)
        self.password_input.delete(0, tk.END)
        self.password_input2.delete(0, tk.END)
        self.name_input.delete(0, tk.END)
        self.lastname_input.delete(0, tk.END)
        self.email_input.delete(0, tk.END)
        self.money_input.delete(0, tk.END)
        self.address_input.delete(0, tk.END)
        super().tkraise()

    def register(self):
        username = self.username_input.get()
        password1 = self.password_input.get()
        password2 = self.password_input2.get()
        name = self.name_input.get()
        lastname = self.lastname_input.get()
        email = self.email_input.get()
        money = self.money_input.get()
        address = self.address_input.get()
        stanowisko = self.stanowisko.get()

        for item in range(len(self.elements)):
            if self.elements[item] == stanowisko:
                stanowisko = self.descriptions_get[item]['id']

        if not username or (not password1 and not password2):
            messagebox.showinfo('Error', 'Podaj login i hasło!')
            return
        if password1 != password2:
            messagebox.showinfo('Error', 'Podano dwa różne hasła!')
            self.register_button.config(bg='ghost white')
            return
        if not name or not lastname:
            messagebox.showinfo('Error', 'Nie podano danych osobowych pracownika!\n'
                                         'Podaj imię i nazwisko.')
            return
        if not email or not address:
            messagebox.showinfo('Error', 'Podaj dane kontaktowe!')
            return
        if not money:
            messagebox.showinfo('Error', 'Pracownik musi mieć pensję!')
            return
        if not stanowisko:
            messagebox.showinfo('Error', 'Pracownik musi mieć stanowisko!')
            return

        login_data = api.get('DaneLogowania', filters={
            'login': username
        })

        if login_data:
            messagebox.showinfo('Error', 'Ten login jest zajęty! Wprowadź ponownie.')
            self.register_button.config(bg='ghost white')
            return

        try:
            dane_logowania = api.create(
                'DaneLogowania',
                attributes={
                    "login": username,
                    "email": email,
                    "haslo": password1
                }
            )
        except Exception:
            messagebox.showinfo('Error', 'Taki adres email nie ma prawa istnieć!.')
            self.register_button.config(bg='ghost white')
            return

        try:
            api.create(
                'Pracownik',
                attributes=
                {
                    "imie": name,
                    "nazwisko": lastname,
                    "adres": address,
                    "wyplata": money
                },
                relationships={
                    'dane_logowania': {
                        'type': 'DaneLogowania',
                        'id': username
                    },
                    "stanowisko": {
                        "type": "Stanowisko",
                        "id": stanowisko
                    }
                })
        except Exception:
            messagebox.showinfo('Error', 'Nie można utworzyć konta pracownika!\n'
                                         'Sprawdź czy wszystkie dane zostały\n'
                                         'prawidłowo wprowadzone.')
            api.delete('DaneLogowania', _id=dane_logowania['id'])
            return

        pracownik = api.get('Pracownik', filters={
            'dane_logowania.login': username
        })
        self.register_button.config(bg='ghost white')
        messagebox.showinfo('Dodano', f'Dodano pracownika: {name}')
        self.controller.set_user(pracownik[0])
        self.controller.show_frame(PracownikPage)
        return

    def tohome(self):
        self.controller.show_frame(PracownikPage)
