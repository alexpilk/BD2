from django.db import models
from django.core import validators


class Lokalizacja(models.Model):
    ulica = models.CharField(max_length=255, verbose_name='Ulica')
    kod_pocztowy = models.CharField(max_length=255, verbose_name='Kod pocztowy')
    miasto = models.CharField(max_length=255, verbose_name='Miasto')

    class Meta:
        verbose_name_plural = 'Lokalizacje'

    def __str__(self):
        return f'{self.ulica}, {self.miasto}'


class RodzajApartamentu(models.Model):
    nazwa = models.CharField(max_length=255, verbose_name='Rodzaj apartamentu', primary_key=True)

    class Meta:
        verbose_name_plural = 'Rodzaje apartamentów'

    def __str__(self):
        return self.nazwa


class OpisApartamentu(models.Model):
    rodzaj = models.ForeignKey(RodzajApartamentu, on_delete=models.CASCADE)
    lokalizacja = models.ForeignKey(Lokalizacja, on_delete=models.CASCADE)
    cena = models.IntegerField(validators=[validators.MinValueValidator(0)], verbose_name='Cena')

    class Meta:
        verbose_name_plural = 'Opisy apartamentów'

    def __str__(self):
        return f'{self.rodzaj} w {self.lokalizacja}'


class Apartament(models.Model):
    opis = models.ForeignKey(OpisApartamentu, on_delete=models.CASCADE)
    zajety = models.BooleanField(verbose_name='Czy zajęty?')

    class Meta:
        verbose_name_plural = 'Apartamenty'

    def __str__(self):
        return f'{"Zajęty" if self.zajety else "Wolny"} {self.opis}'
