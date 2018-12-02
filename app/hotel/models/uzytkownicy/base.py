from django.db import models


class DaneLogowania(models.Model):
    login = models.CharField(max_length=255, verbose_name='Login', primary_key=True)
    email = models.EmailField(verbose_name='Adres mailowy')
    haslo = models.CharField(max_length=255, verbose_name='Hasło')

    class Meta:
        verbose_name_plural = 'Dane logowania'

    def __str__(self):
        return 'Dane logowania dla {self.login}'


class Uzytkownik(models.Model):
    imie = models.CharField(max_length=255, verbose_name='Imię')
    nazwisko = models.CharField(max_length=255, verbose_name='Nazwisko')
    adres = models.CharField(max_length=255, verbose_name='Adres zamieszkania')
    dane_logowania = models.OneToOneField(DaneLogowania, on_delete=models.CASCADE)

    class Meta:
        abstract = True

