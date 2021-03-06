import tkinter as tk
from . import frames
from inspect import isclass


class HotelApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.user_data = {}

        for module_name in dir(frames):
            obj = getattr(frames, module_name)
            if isclass(obj) and issubclass(obj, tk.Frame):
                frame = obj(container, self)
                self.frames[obj] = frame
                frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(frames.LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def set_user(self, user_data):
        self.user_data = user_data

    def get_user(self):
        return self.user_data

    info_o_programie = 'Aplikacja obsługująca ośrodek wypoczynkowy\n\n' \
                                                      'AUTORZY:\n' \
                                                      '     Oleksii Pilkevych\n' \
                                                      '     Iwona Wachowska\n' \
                                                      '     Filip Kądziołka\n\n' \
                                                      'Projekt studencki na kursie:\n' \
                                                      '     BAZY DANYCH 2\n' \
                                                      'Prowadzący:\n' \
                                                      '     dr.inż.Jarosław Rudy\n' \
                                                      'Uczelnia:\n' \
                                                      '     Politechnika Wrocławska\n\n' \
                                                      ' * oprogramowanie powstało dzięki wsparciu sponsorów.'
