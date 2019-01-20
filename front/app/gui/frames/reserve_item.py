import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
from app.api import api
import tkcalendar

# nie działa do końca wybieranie apartamentu... bez zaznaczenia niczego,
# automatycznie wybiera pozycję pierwszą i podaje ją jako wybraną

class ItemReservePage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.item_list = tk.Listbox(self)
        self.item_list.config(height=10, width=60, selectmode='browse')

        self.start_date_label = tk.Label(self)
        self.start_date_input = tk.Entry(self)
        self.end_date_label = tk.Label(self)
        self.end_date_input = tk.Entry(self)

        self.reserve_apartment_button = tk.Button(self, text="Rezerwuj sprzęt", command=self.reserve_item)
        self.return_button = tk.Button(self, text="Wróć do strony głównej", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Rezerwacja sprzętu")
        self.start_date_label.config(text="Data rozpoczęcia rezerwacji:")
        self.end_date_label.config(text="Data zakończenia rezerwacji:")

        self.item_list.delete(0, tk.END)

        self.apps_get = []
        self.apps_get = api.get(
            'Sprzet',
            fields={
                "IdSprzetu": ['id'],
                "NazwaSprzetu": ['verbose_name']
            },
            filters={
                'zajety': False
            }
        )

        self.elements = []
        for i in range(len(self.apps_get)):
            self.elements.append(self.apps_get[i]['verbose_name'])

        for item in self.elements:
            self.item_list.insert(tk.END, item)

        self.item_list.activate(0)
        self.item_list.selection_set(0, 0)
        self.start_date_input.delete(0, tk.END)
        self.start_date_input.insert(0, "yyyy-mm-dd")
        self.end_date_input.delete(0, tk.END)
        self.end_date_input.insert(0, "yyyy-mm-dd")

        self.start_date_label.pack()
        self.start_date_input.pack()
        self.end_date_label.pack()
        self.end_date_input.pack()
        self.item_list.pack()
        self.reserve_apartment_button.pack()
        self.return_button.pack()
        super().tkraise()

    def reserve_item(self):
        item_id = self.item_list.get(tk.ACTIVE)
        new_id = self.controller.user_data["id"]
        start_date = self.start_date_input.get()
        end_date = self.end_date_input.get()

        for item in range(len(self.elements)):
            if self.elements[item] == item_id:
                item_id = self.apps_get[item]['id']
        if not item_id or not start_date or not end_date:
            messagebox.showinfo('Error', 'Wybierz sprzęt i podaj daty!')

        self.dane = api.get(
            'Sprzet',
            filters={
                'id': item_id
            },
            include=[
                'opis'
            ]
        )

        try:
            reservation = api.create(
                'RezerwacjaSprzetu',
                attributes={
                    "data_wypozyczenia": start_date,
                    "data_zwrotu": end_date
                },
                relationships={
                    'klient': {
                        'type': 'Klient',
                        'id': self.controller.user_data['id']
                    },
                    'sprzet': {
                        'type': 'Sprzet',
                        'id': item_id
                    }
                })
        except Exception:
            messagebox.showinfo('Error', 'Nie można utworzyć rezerwacji apartamentu! '
                                         'Sprawdź czy wszystkie dane (np. daty) zostały '
                                         'prawidłowo wprowadzone.')
            return

        try:

            api.update(
                'Sprzet',
                attributes={
                    "zajety": True
                },
                relationships={
                    'opis': {
                        'type': 'OpisSprzetu',
                        'id': self.dane[0]['opis']['id']
                    }
                },
                _id=item_id
            )
        except Exception:
            api.delete('RezerwacjeApartamentow', _id=reservation['id'])
            messagebox.showinfo('Error', 'Nie można ustawić apartamentu na zajęty! '
                                         'Sprawdź czy wszystkie dane (np. daty) zostały '
                                         'prawidłowo wprowadzone.')
            return

        messagebox.showinfo('Error', f'Dodano nową rezerwację od: {reservation["data_wypozyczenia"]}\n'
                                     f'Ustawiono sprzęt na zajęty.')

    def tohome(self):
        self.controller.show_frame(frames.KlientPage)

