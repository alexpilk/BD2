import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
# from .register_pracownik import RegisterPrac
from app.api import api

class ItemAddPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.descriptions_get = []
        self.descriptions_get = api.get(
            'OpisSprzetu',
            fields={
                "IdSprzetu": ['id'],
                "OpisSprzetu": ['verbose_name']
            }
        )

        self.elements = []
        for i in range(len(self.descriptions_get)):
            self.elements.append(self.descriptions_get[i]['verbose_name'])

        self.descr_label = tk.Label(self)
        self.opis = tk.StringVar(self)
        self.descr_list = tk.OptionMenu(self, self.opis, *self.elements)

        self.size_label = tk.Label(self)
        self.size_input = tk.Entry(self)

        self.status_label = tk.Label(self)
        self.status = tk.StringVar(self)
        self.status_list = tk.OptionMenu(self, self.status, "Wolny", "Zajęty")

        self.checkdate_label = tk.Label(self)
        # dodać datę przeglądu... omg...

        self.add_descr_button = tk.Button(self, text="Dodaj nowy opis sprzętu", command=self.add_desription)
        self.add_button = tk.Button(self, text="Dodaj nowy sprzęt", command=self.add_item)
        self.return_button = tk.Button(self, text="Wróć do strony pracownika", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Dodawanie nowego sprzętu:")
        self.descr_label.config(text="Rodzaj sprzętu:")
        self.size_label.config(text="Rozmiar:")
        self.checkdate_label.config(text="Data kolejnego przeglądu:")
        self.status_label.config(text="Status:")
        self.add_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')
        self.add_descr_button.config(bg='ghost white')

        self.opis.set("---")
        self.status.set("---")
        self.size_input.delete(0, tk.END)

        self.descr_label.pack()
        self.descr_list.pack()
        self.size_label.pack()
        self.size_input.pack()
        self.checkdate_label.pack()

        self.status_label.pack()
        self.status_list.pack()
        self.add_descr_button.pack()
        self.add_button.pack()
        self.return_button.pack()
        super().tkraise()

    def add_item(self):
        description = self.opis.get()
        for item in range(len(self.elements)):
            if self.elements[item] == description:
                description = self.descriptions_get[item]['id']
        size = self.size_input.get()
        status = self.status.get()


        if not description or not status or not size:
            messagebox.showinfo('Error', 'Podaj dane sprzętu!')
            return

        if status == 'wolny':
            try:
                item = api.create(
                    'Sprzet',
                    attributes={
                        "rozmiar": size,
                        "zajety": False,
                        "termin_przegladu": "2019-03-01T09:00:00Z"
                    },
                    relationships={
                        'opis': {
                            'type': 'OpisSprzetu',
                            'id': description
                        }
                    })
            except Exception:
                messagebox.showinfo('Error', 'Nie można utworzyć wolnego sprzętu! '
                                             'Sprawdź czy wszystkie dane zostały '
                                             'prawidłowo wprowadzone.')
                return
        else:
            try:
                item = api.create(
                    'Sprzet',
                    attributes={
                        "rozmiar": size,
                        "zajety": True,
                        "termin_przegladu": "2019-03-01T09:00:00Z"
                    },
                    relationships={
                        'opis': {
                            'type': 'OpisSprzetu',
                            'id': description
                        }
                    })
            except Exception:
                messagebox.showinfo('Error', 'Nie można utworzyć zajętego sprzętu! '
                                             'Sprawdź czy wszystkie dane zostały '
                                             'prawidłowo wprowadzone.')
                return
        messagebox.showinfo('Info', f'Utworzono nowy: {item["verbose_name"]}.')

    def add_desription(self):
        self.controller.show_frame(frames.AddItemDescription)

    def tohome(self):
        self.controller.show_frame(frames.PracownikPage)

