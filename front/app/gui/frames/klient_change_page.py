import tkinter as tk
from tkinter import messagebox

from app.api import api
from app.gui import frames

from .base import BaseFrame
from .klient_home import KlientPage


class KlientChangePage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

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
        self.card_label = tk.Label(self)
        self.card_input = tk.Entry(self)
        self.address_label = tk.Label(self)
        self.address_input = tk.Entry(self)
        self.register_button = tk.Button(self, text="Zmień dane", command=self.register)
        self.return_button = tk.Button(self, text="Wróć do strony głównej", command=self.tohome)

        self.register_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')

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
        self.card_label.pack()
        self.card_input.pack()
        self.address_label.pack()
        self.address_input.pack()
        self.register_button.pack()
        self.return_button.pack()

    def tkraise(self, *args, **kwargs):
        self.label.config(text=f"Zmiana danych osobowych:")
        self.password_label.config(text="Hasło:")
        self.password_label2.config(text="Powtórz hasło:")
        self.name_label.config(text="Imię:")
        self.lastname_label.config(text="Nazwisko:")
        self.email_label.config(text="Adres email:")
        self.card_label.config(text="Numer karty płatniczej:")
        self.address_label.config(text="Adres zamieszkania:")

        self.dane = api.get(
            'Klient',
            filters={
                'id': self.controller.user_data['id']
            },
            include=[
                'dane_logowania'
            ]
        )

        self.password_input.delete(0, tk.END)
        self.password_input.insert(0, self.dane[0]['dane_logowania']['haslo'])
        self.password_input2.delete(0, tk.END)
        self.password_input2.insert(0, self.dane[0]['dane_logowania']['haslo'])
        self.name_input.delete(0, tk.END)
        self.name_input.insert(0, self.dane[0]['imie'])
        self.lastname_input.delete(0, tk.END)
        self.lastname_input.insert(0, self.dane[0]['nazwisko'])
        self.email_input.delete(0, tk.END)
        self.email_input.insert(0, self.dane[0]['dane_logowania']['email'])
        self.card_input.delete(0, tk.END)
        self.card_input.insert(0, self.dane[0]['numer_karty'])
        self.address_input.delete(0, tk.END)
        self.address_input.insert(0, self.dane[0]['adres'])
        super().tkraise()

    def register(self):
        password1 = self.password_input.get()
        password2 = self.password_input2.get()
        name = self.name_input.get()
        lastname = self.lastname_input.get()
        email = self.email_input.get()
        card = self.card_input.get()
        address = self.address_input.get()

        if not password1 and not password2:
            messagebox.showinfo('Error', 'Podaj hasło!')
            self.register_button.config(bg='ghost white')
            return
        if password1 != password2:
            messagebox.showinfo('Error', 'Podano dwa różne hasła!')
            self.register_button.config(bg='ghost white')
            return
        if not name or not lastname:
            messagebox.showinfo('Error', 'Potrzebujemy Twoich danych osobowych! '
                                         'Podaj imię i nazwisko.')
            self.register_button.config(bg='ghost white')
            return
        if not email or not address or not card:
            messagebox.showinfo('Error', 'Ptrzebujemy Twoich danych kontaktowych! '
                                         'Podaj swój adres email, adres zamieszkania i numer karty.')
            self.register_button.config(bg='ghost white')
            return

        if password1==self.dane[0]['dane_logowania']['haslo'] and (name==self.dane[0]['imie'])and (lastname==self.dane[0]['nazwisko']):
            if (email==self.dane[0]['dane_logowania']['email']) and (card==self.dane[0]['numer_karty']) and (address == self.dane[0]['adres']):
                messagebox.showinfo('Error', 'Nie wprowadzono żadnych zmian! ')
                return

        if not (len(card) == 19) or not (card[4] == ' ') or not (card[9] == ' ') or not (card[14] == ' '):
            messagebox.showinfo('Error', 'Podano nieprawidłowy numer karty!')
            return

        try:
            api.update(
                'DaneLogowania',
                attributes={
                    "login": self.dane[0]['dane_logowania']['login'],
                    "email": email,
                    "haslo": password1
                },
                _id=self.dane[0]['dane_logowania']['login']
            )
        except Exception:
            messagebox.showinfo('Error', 'Taki adres email nie ma prawa istnieć!.')
            self.register_button.config(bg='ghost white')
            return
        try:
           api.update(
               'Klient',
               attributes=
               {
                   "imie": name,
                   "nazwisko": lastname,
                   "adres": address,
                   "numer_karty": card
               },
               relationships={
                   'dane_logowania': {
                       'type': 'DaneLogowania',
                       'id': self.dane[0]['dane_logowania']['login']
                   }
               },
               _id=self.dane[0]['id']
           )
        except Exception:
            messagebox.showinfo('Error', 'Nie udało się zaktualizować danych!\n'
                                         'Sprawdź, czy wszystkie wartości są\n'
                                         'prawidłowo wprowadzone.')
            return

        klient = api.get('Klient', filters={
            'dane_logowania.login': self.dane[0]['dane_logowania']['login']
        })
        self.register_button.config(bg='ghost white')
        messagebox.showinfo('Zmieniono', f'Zmieniono dane klienta: {(name)}')
        self.controller.set_user(klient[0])
        self.controller.show_frame(KlientPage)

    def tohome(self):
        self.controller.show_frame(frames.KlientPage)
