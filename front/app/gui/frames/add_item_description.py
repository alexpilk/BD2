import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
from app.api import api


class AddItemDescription(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.type_get = []
        self.type_get = api.get(
            'RodzajSprzetu',
            fields={
                "IdTypu": ['id'],
                "NazwaTypu": ['nazwa']
            }
        )

        self.type_elements = []
        for i in range(len(self.type_get)):
            self.type_elements.append(self.type_get[i]['nazwa'])

        self.type_label = tk.Label(self)
        self.opis = tk.StringVar(self)
        self.type_list = tk.OptionMenu(self, self.opis, *self.type_elements)

        self.mark_get = []
        self.mark_get = api.get(
            'Producent',
            fields={
                "IdProducenta": ['id'],
                "NazwaProducenta": ['nazwa']
            }
        )

        self.mark_elements = []
        for i in range(len(self.mark_get)):
            self.mark_elements.append(self.mark_get[i]['nazwa'])

        self.mark_label = tk.Label(self)
        self.opis1 = tk.StringVar(self)
        self.location_list = tk.OptionMenu(self, self.opis1, *self.mark_elements)

        self.price_label = tk.Label(self)
        self.price_input = tk.Entry(self)

        self.add_button = tk.Button(self, text="Dodaj opis", command=self.add_desc)
        self.return_button = tk.Button(self, text="Wróć do strony głównej", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Dodawanie nowego opisu sprzętu:")
        self.type_label.config(text="Rodzaj sprzętu:")
        self.mark_label.config(text="Producent:")
        self.price_label.config(text="Cena za godzinę:")
        self.add_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')

        self.price_input.delete(0, tk.END)
        self.opis.set("---")
        self.opis1.set("---")

        self.type_label.pack()
        self.type_list.pack()
        self.mark_label.pack()
        self.location_list.pack()
        self.price_label.pack()
        self.price_input.pack()
        self.add_button.pack()
        self.return_button.pack()
        super().tkraise()

    def add_desc(self):
        price = self.price_input.get()
        ittype = self.opis.get()
        for item in range(len(self.type_elements)):
            if self.type_elements[item] == ittype:
                ittype = self.type_get[item]['id']

        mark = self.opis1.get()
        for item in range(len(self.mark_elements)):
            if self.mark_elements[item] == mark:
                mark = self.mark_get[item]['id']

        if not ittype or not mark or not price:
            messagebox.showinfo('Error', 'Podaj rodzaj, producenta i cenę!')
            return

        if (ittype == '---') or (mark == '---'):
            messagebox.showinfo('Error', 'Podaj rodzaj i producenta!')
            return

        try:
            new_descript = api.create(
                'OpisSprzetu',
                attributes={
                    'cena': price
                },
                relationships={
                    'rodzaj': {
                        'type': 'RodzajSprzetu',
                        'id': ittype
                    },
                    'producent': {
                        'type': 'Producent',
                        'id': mark
                    }
                })
        except Exception:
            messagebox.showinfo('Error', 'Nie można utworzyć opisu sprzętu!\n'
                                         'Sprawdź czy wszystkie dane zostały\n'
                                         'prawidłowo wprowadzone.')
            return
        messagebox.showinfo('Info', f'Utworzono nowy: {(new_descript["verbose_name"])}.')

    def tohome(self):
        self.controller.show_frame(frames.PracownikPage)

