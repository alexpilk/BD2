from django.db import models

from .base import Uzytkownik


class Klient(Uzytkownik):
    numer_karty = models.CharField(max_length=255, verbose_name='Numer karty')

    class Meta:
        verbose_name_plural = 'Klienci'

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'
