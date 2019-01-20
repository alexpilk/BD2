import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
from app.api import api
import tkcalendar

# nie działa do końca wybieranie apartamentu... bez zaznaczenia niczego,
# automatycznie wybiera pozycję pierwszą i podaje ją jako wybraną

class ApartmentReservePage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.apartment_list = tk.Listbox(self)
        self.apartment_list.config(height=10, width=60, selectmode='browse')

        self.start_date_label = tk.Label(self)
        self.start_date_input = tk.Entry(self)
        self.end_date_label = tk.Label(self)
        self.end_date_input = tk.Entry(self)

        self.reserve_apartment_button = tk.Button(self, text="Rezerwuj apartament", command=self.reserve_apartment)
        self.return_button = tk.Button(self, text="Wróć do strony głównej", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Rezerwacja apartamentu")
        self.start_date_label.config(text="Data rozpoczęcia rezerwacji:")
        self.end_date_label.config(text="Data zakończenia rezerwacji:")

        self.apartment_list.delete(0, tk.END)

        self.apps_get = []
        self.apps_get = api.get(
            'Apartament',
            fields={
                "IdApartamentu": ['id'],
                "NazwaApartamentu": ['verbose_name']
            },
            filters={
                'zajety': False
            }
        )

        self.elements = []
        for i in range(len(self.apps_get)):
            self.elements.append(self.apps_get[i]['verbose_name'])

        for item in self.elements:
            self.apartment_list.insert(tk.END, item)

        self.apartment_list.activate(0)
        self.apartment_list.selection_set(0,0)
        self.start_date_input.delete(0, tk.END)
        self.start_date_input.insert(0, "yyyy-mm-dd")
        self.end_date_input.delete(0, tk.END)
        self.end_date_input.insert(0, "yyyy-mm-dd")

        self.start_date_label.pack()
        self.start_date_input.pack()
        self.end_date_label.pack()
        self.end_date_input.pack()
        self.apartment_list.pack()
        self.reserve_apartment_button.pack()
        self.return_button.pack()
        super().tkraise()

    def reserve_apartment(self):
        apartment = self.apartment_list.get(tk.ACTIVE)
        new_id = self.controller.user_data["id"]
        start_date = self.start_date_input.get()
        end_date = self.end_date_input.get()

        for item in range(len(self.elements)):
            if self.elements[item] == apartment:
                apartment = self.apps_get[item]['id']
        if not apartment or not start_date or not end_date:
            messagebox.showinfo('Error', 'Wybierz apartament i podaj daty!')

        self.dane = api.get(
            'Apartament',
            filters={
                'id': apartment
            },
            include=[
                'opis'
            ]
        )

        try:
            reservation = api.create(
                'RezerwacjeApartamentow',
                attributes={
                    "data_wynajecia": start_date,
                    "data_wymeldowania": end_date
                },
                relationships={
                    'klient': {
                        'type': 'Klient',
                        'id': self.controller.user_data['id']
                    },
                    'apartament': {
                        'type': 'Apartament',
                        'id': apartment
                    }
                })
        except Exception:
            messagebox.showinfo('Error', 'Nie można utworzyć rezerwacji apartamentu! '
                                         'Sprawdź czy wszystkie dane (np. daty) zostały '
                                         'prawidłowo wprowadzone.')
            return

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
                _id=apartment
            )
        except Exception:
            api.delete('RezerwacjeApartamentow', _id=reservation['id'])
            messagebox.showinfo('Error', 'Nie można ustawić apartamentu na zajęty! '
                                         'Sprawdź czy wszystkie dane (np. daty) zostały '
                                         'prawidłowo wprowadzone.')
            return

        messagebox.showinfo('Error', f'Dodano nową rezerwację od: {reservation["data_wynajecia"]}\n'
                                     f'Ustawiono apartament na zajęty.')

    def tohome(self):
        self.controller.show_frame(frames.KlientPage)

