import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
from app.api import api
import tkcalendar


class AppReturnPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.reservations_get = []
        self.elements = []
        self.dane = []

        self.res_label = tk.Label(self)
        self.reservation_list = tk.Listbox(self)
        self.reservation_list.config(height=10, width=85, selectmode='browse')

        self.filter_res_label = tk.Label(self)
        self.filter_res_input = tk.Entry(self)
        self.filter_res_button = tk.Button(self, text="Wyszukaj rezerwację", command=self.filter_res)
        self.return_app_button = tk.Button(self, text="Wymelduj z apartamentu", command=self.return_item)
        self.return_button = tk.Button(self, text="Wróć do strony głównej", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Wymelduj gościa z apartamentu")
        self.res_label.config(text="Wybierz rezerwację:")
        self.filter_res_label.config(text="Wprowadź nazwisko rezerwującego:")
        self.filter_res_input.delete(0, tk.END)

        # self.filter_res_input.insert(0, "Baggins")

        self.reservation_list.delete(0, tk.END)

        self.reservations_get = []
        self.reservations_get = api.get(
            'RezerwacjeApartamentow',
            fields={
                "Idrezerwacji": ['id'],
                "Nazwarezerwacji": ['verbose_name']
            },
            include={
                'apartament':{
                    "IdApartamentu": ['id']
                }
            }
        )

        self.elements = [reservation['verbose_name'] for reservation in self.reservations_get]

        for item in self.elements:
            self.reservation_list.insert(tk.END, item)

        self.reservation_list.activate(0)
        self.reservation_list.selection_set(0, 0)

        self.res_label.pack()
        self.reservation_list.pack()
        self.filter_res_label.pack()
        self.filter_res_input.pack()
        self.filter_res_button.pack()
        self.return_app_button.pack()
        self.return_button.pack()
        super().tkraise()

    def return_item(self):
        res_id = self.reservation_list.get(tk.ACTIVE)
        app_id = 0

        for appart in range(len(self.elements)):
            if self.elements[appart] == res_id:
                res_id = self.reservations_get[appart]['id']
                app_id = self.reservations_get[appart]['apartament']['id']
        if not res_id:
            messagebox.showinfo('Error', 'Wybierz rezerwację!')
            return

        # messagebox.showinfo('Error', f'Dane:\n'
        #                              f'Rezka: {res_id}\n'
        #                              f'Apek: {app_id}\n')

        self.dane = api.get(
            'Apartament',
            fields={
                "ItemId": 'id',
                "CzyZajety": 'zajety'
            },
            filters={
                'id': app_id
            },
            include={
                'opis'
            }
        )

        # messagebox.showinfo('Error', f'Dotyczy apu: {self.dane}')

        try:
            api.update(
                'Apartament',
                attributes={
                    "zajety": False
                },
                relationships={
                    'opis': {
                        'type': 'OpisApartamentu',
                        'id': self.dane[0]['opis']['id']
                    }
                },
                _id=app_id
            )
        except Exception:
            messagebox.showinfo('Error', 'Nie ustawiono apartamentu na wolny!\n'
                                         'Sprawdź czy wszystkie dane zostały\n'
                                         'prawidłowo wprowadzone.')
            return

        try:
            api.delete('RezerwacjeApartamentow', _id=res_id)
        except Exception:
            messagebox.showinfo('Error', 'Nie można usunąć wybranej rezerwacji!\n'
                                         'Sprawdź, czy wszystkie dane zostały podane prawidłowo.')
            try:
                api.update(
                    'Apartament',
                    attributes={
                        "zajety": True
                    },
                    relationships={
                        'opis': {
                            'type': 'OpisApartamentu',
                            'id': self.dane[0]['opis']['id']
                        }
                    },
                    _id=app_id
                )
            except Exception:
                messagebox.showinfo('Error', 'Nie ustawiono apartamentu na wolny!\n'
                                             'Sprawdź czy wszystkie dane zostały\n'
                                             'prawidłowo wprowadzone.')
                return
            return

        messagebox.showinfo('Info', f'Udało się wymeldować gości.')

    def filter_res(self):
        # messagebox.showinfo('Info', 'Tego jeszcze nie ma ;)')

        nazwisko = self.filter_res_input.get()
        if not nazwisko:
            messagebox.showinfo('Info', 'Nie wpisano kryterium!')
            return

        klient_id = api.get(
            'Klient',
            fields={
                "KlientId": ['id']
            },
            filters={
                'nazwisko': nazwisko
            }
        )

        if not klient_id:
            messagebox.showinfo('Info', 'Nie znalezino takiego klienta!')
            return

        # messagebox.showinfo('Info', f'Klient id: {klient_id[0]["id"]}')

        self.reservation_list.delete(0, tk.END)

        self.reservations_get = []
        self.reservations_get = api.get(
            'RezerwacjeApartamentow',
            fields={
                "Idrezerwacji": ['id'],
                "Nazwarezerwacji": ['verbose_name']
            },
            filters={
                'klient.id': klient_id[0]["id"]
            }
        )

        self.elements.clear()
        for i in range(len(self.reservations_get)):
            self.elements.append(self.reservations_get[i]['verbose_name'])

        for item in self.elements:
            self.reservation_list.insert(tk.END, item)

        self.reservation_list.activate(0)
        self.reservation_list.selection_set(0, 0)

    def tohome(self):
        self.controller.show_frame(frames.PracownikPage)

