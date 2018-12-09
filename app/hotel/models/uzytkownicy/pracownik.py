from django.core import validators
from django.db import models

from .base import Uzytkownik


class TypBonuPracowniczego(models.Model):
    nazwa = models.CharField(max_length=255, verbose_name='Typ', primary_key=True)

    class Meta:
        verbose_name_plural = 'Typy bonów pracowniczych'

    def __str__(self):
        return self.nazwa


class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=255, verbose_name='Stanowisko', primary_key=True)

    class Meta:
        verbose_name_plural = 'Stanowiska'

    def __str__(self):
        return self.nazwa


class BonPracowniczy(models.Model):
    typ = models.ForeignKey(TypBonuPracowniczego, on_delete=models.CASCADE)
    stanowisko = models.ManyToManyField(Stanowisko)

    class Meta:
        verbose_name_plural = 'Bony pracownicze'

    def __str__(self):
        stanowiska = ', '.join([str(stanowisko) for stanowisko in self.stanowisko.all()])
        return f'{self.typ} dla {stanowiska}'


class Pracownik(Uzytkownik):
    wyplata = models.IntegerField(verbose_name='Wypłata', validators=[validators.MinValueValidator(0)])
    stanowisko = models.ForeignKey(Stanowisko, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Pracownicy'

    def __str__(self):
        return f'{self.imie} {self.nazwisko} ({self.stanowisko})'
