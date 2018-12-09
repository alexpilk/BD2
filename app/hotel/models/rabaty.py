from django.db import models
from django.core import validators
from .uzytkownicy import Klient


class TypRabatu(models.Model):
    typ = models.CharField(max_length=255, primary_key=True, verbose_name='Typy rabatu')

    class Meta:
        verbose_name_plural = 'Typy rabatów'

    def __str__(self):
        return f'Rabat na {self.typ}'


class Rabat(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    procent_znizki = models.IntegerField(validators=[validators.MinValueValidator(0),
                                                     validators.MaxValueValidator(100)], verbose_name='Procent zniżki')
    typ = models.ForeignKey(TypRabatu, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Rabaty'

    def __str__(self):
        return f'{self.procent_znizki}% {self.typ}'
