from django.core import validators
from django.db import models

from .apartamenty import Apartament
from .sprzet import Sprzet
from .uzytkownicy import Klient, Pracownik


class Rezerwacja(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class RezerwacjaSprzetu(Rezerwacja):
    sprzet = models.ForeignKey(Sprzet, on_delete=models.CASCADE)
    data_wypozyczenia = models.DateField(verbose_name='Data wypożyczenia')
    data_zwrotu = models.DateField(verbose_name='Data zwrotu')

    class Meta:
        verbose_name_plural = 'Rezerwacje sprzętu'

    def __str__(self):
        return f'Rezerwacja {self.sprzet} dla {self.klient}'


class RezerwacjeApartamentow(Rezerwacja):
    apartament = models.ForeignKey(Apartament, on_delete=models.CASCADE)
    data_wynajecia = models.DateField(verbose_name='Data wynajęcia')
    data_wymeldowania = models.DateField(verbose_name='Data wymeldowania')

    class Meta:
        verbose_name_plural = 'Rezerwacje apartamentów'

    def __str__(self):
        return f'Rezerwacja apartamentu {self.apartament}'


class PotwierdzenieZwrotu(models.Model):
    pracownik = models.ForeignKey(Pracownik, on_delete=models.CASCADE)
    rezerwacja = models.OneToOneField(RezerwacjeApartamentow, on_delete=models.CASCADE,
                                      related_name='potwierdzenie_zwrotu')

    class Meta:
        verbose_name_plural = 'Potwierdzenia zwrotów'

    def __str__(self):
        return f'Potwierdził {self.pracownik}. {self.rezerwacja}'


class PotwierdzenieWplaty(models.Model):
    kwota = models.IntegerField(verbose_name='Kwota', validators=[validators.MinValueValidator(0)])
    data = models.DateField(verbose_name='Data dokonania')
    rezerwacja = models.OneToOneField(RezerwacjeApartamentow, on_delete=models.CASCADE,
                                      related_name='potwierdzenie_wplaty')

    class Meta:
        verbose_name_plural = 'Potwierdzenia wpłat'

    def __str__(self):
        return f'{self.kwota} wpłacona {self.data}. {self.rezerwacja}'
