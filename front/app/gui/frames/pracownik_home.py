import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames


class PracownikPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.return_item_button = tk.Button(self, text="Zwróć sprzęt", command=self.return_item)
        self.return_app_button = tk.Button(self, text="Wymelduj gościa", command=self.return_app)

        self.menubar = tk.Menu(self.controller)
        self.danemenu = tk.Menu(self.menubar, tearoff=0)
        self.danemenu.add_command(label="Zmień swoje dane", command=self.change_info)
        self.danemenu.add_command(label="Dodaj klienta", command=self.addclient)
        self.danemenu.add_command(label="Dodaj pracownika", command=self.addworker)

        self.appManagemenu = tk.Menu(self.menubar, tearoff=0)
        self.appManagemenu.add_command(label="Dodaj apartament", command=self.addapartment)
        self.appManagemenu.add_command(label="Dodaj opis apartamentu", command=self.add_app_desription)

        self.itemManagemenu = tk.Menu(self.menubar, tearoff=0)
        self.itemManagemenu.add_command(label="Dodaj sprzęt", command=self.additem)
        self.itemManagemenu.add_command(label="Dodaj opis sprzętu", command=self.add_item_desription)

        self.menubar.add_cascade(label="Apartamenty", menu=self.appManagemenu)
        self.menubar.add_cascade(label="Sprzęt", menu=self.itemManagemenu)
        self.menubar.add_cascade(label="Użytkownicy", menu=self.danemenu)
        self.menubar.add_command(label="O programie", command=self.program_info)
        self.menubar.add_command(label="Wyloguj", command=self.logout)

    def tkraise(self, *args, **kwargs):
        self.label.config(text=f"Witamy na stronie pracownika, {self.controller.user_data['imie']}")
        self.return_item_button.config(bg='ghost white')
        self.return_item_button.pack()
        self.return_app_button.config(bg='ghost white')
        self.return_app_button.pack()
        self.controller.config(menu=self.menubar)
        super().tkraise()

    def addworker(self):
        self.controller.show_frame(frames.RegisterPrac)

    def addclient(self):
        self.controller.show_frame(frames.RegisterKli)

    def addapartment(self):
        self.controller.show_frame(frames.ApartmentAddPage)

    def add_app_desription(self):
        self.controller.show_frame(frames.AddApartmentDescription)

    def add_item_desription(self):
        self.controller.show_frame(frames.AddItemDescription)

    def additem(self):
        self.controller.show_frame(frames.ItemAddPage)

    def return_item(self):
        self.controller.show_frame(frames.ItemReturnPage)

    def return_app(self):
        self.controller.show_frame(frames.AppReturnPage)

    def change_info(self):
        self.controller.show_frame(frames.PracownikChangePage)

    def logout(self):
        self.controller.set_user(0)
        self.controller.show_frame(frames.LoginPage)

    def program_info(self):
        messagebox.showinfo('Informacje o programie', self.controller.info_o_programie)





