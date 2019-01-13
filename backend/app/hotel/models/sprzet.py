from django.db import models
from django.core import validators


class Producent(models.Model):
    nazwa = models.CharField(max_length=255, verbose_name='Producent', primary_key=True)

    class Meta:
        verbose_name_plural = 'Producenci'

    def __str__(self):
        return self.nazwa


class RodzajSprzetu(models.Model):
    nazwa = models.CharField(max_length=255, verbose_name='Rodzaj sprzętu', primary_key=True)

    class Meta:
        verbose_name_plural = 'Rodzaje sprzętu'

    def __str__(self):
        return self.nazwa


class OpisSprzetu(models.Model):
    rodzaj = models.ForeignKey(RodzajSprzetu, on_delete=models.CASCADE)
    producent = models.ForeignKey(Producent, on_delete=models.CASCADE)
    cena = models.IntegerField(validators=[validators.MinValueValidator(0)], verbose_name='Cena')

    class Meta:
        verbose_name_plural = 'Opisy sprzętu'

    def __str__(self):
        return f'{self.rodzaj} od {self.producent}'


class Sprzet(models.Model):
    opis = models.ForeignKey(OpisSprzetu, on_delete=models.CASCADE)
    rozmiar = models.IntegerField(validators=[validators.MinValueValidator(0)], verbose_name='Rozmiar')
    termin_przegladu = models.DateTimeField(verbose_name='Termin przeglądu')
    zajety = models.BooleanField(verbose_name='Czy zajęty?')

    class Meta:
        verbose_name_plural = 'Sprzęt'

    def __str__(self):
        return f'{self.opis} o rozmiarze {self.rozmiar}'
