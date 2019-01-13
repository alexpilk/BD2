from rest_framework_json_api import serializers
from . import models


class DaneLogowaniaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DaneLogowania
        fields = '__all__'


class KlientSerializer(serializers.ModelSerializer):
    included_serializers = {
        'dane_logowania': 'hotel.serializers.DaneLogowaniaSerializer',
    }

    class Meta:
        model = models.Klient
        fields = '__all__'


class PracownikSerializer(serializers.ModelSerializer):
    included_serializers = {
        'dane_logowania': 'hotel.serializers.DaneLogowaniaSerializer',
        'stanowisko': 'hotel.serializers.StanowiskoSerializer',
    }

    class Meta:
        model = models.Pracownik
        fields = '__all__'


class BonPracowniczySerializer(serializers.ModelSerializer):
    included_serializers = {
        'typ': 'hotel.serializers.TypBonuPracowniczegoSerializer',
        'stanowisko': 'hotel.serializers.StanowiskoSerializer',
    }

    class Meta:
        model = models.BonPracowniczy
        fields = '__all__'


class TypBonuPracowniczegoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TypBonuPracowniczego
        fields = '__all__'


class StanowiskoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Stanowisko
        fields = '__all__'


class ApartamentSerializer(serializers.ModelSerializer):
    included_serializers = {
        'opis': 'hotel.serializers.OpisApartamentuSerializer',
    }

    class Meta:
        model = models.Apartament
        fields = '__all__'


class OpisApartamentuSerializer(serializers.ModelSerializer):
    included_serializers = {
        'rodzaj': 'hotel.serializers.RodzajApartamentuSerializer',
        'lokalizacja': 'hotel.serializers.LokalizacjaSerializer',
    }

    class Meta:
        model = models.OpisApartamentu
        fields = '__all__'


class LokalizacjaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lokalizacja
        fields = '__all__'


class RodzajApartamentuSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RodzajApartamentu
        fields = '__all__'


class RabatSerializer(serializers.ModelSerializer):
    included_serializers = {
        'klient': 'hotel.serializers.KlientSerializer',
        'typ': 'hotel.serializers.TypRabatuSerializer',
    }

    class Meta:
        model = models.Rabat
        fields = '__all__'


class TypRabatuSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TypRabatu
        fields = '__all__'


class RezerwacjaSprzetuSerializer(serializers.ModelSerializer):
    included_serializers = {
        'klient': 'hotel.serializers.KlientSerializer',
        'sprzet': 'hotel.serializers.SprzetSerializer',
    }

    class Meta:
        model = models.RezerwacjaSprzetu
        fields = '__all__'


class RezerwacjeApartamentowSerializer(serializers.ModelSerializer):
    included_serializers = {
        'klient': 'hotel.serializers.KlientSerializer',
        'apartament': 'hotel.serializers.ApartamentSerializer',
    }

    class Meta:
        model = models.RezerwacjeApartamentow
        fields = '__all__'


class PotwierdzenieWplatySerializer(serializers.ModelSerializer):
    included_serializers = {
        'rezerwacja': 'hotel.serializers.RezerwacjeApartamentowSerializer',
    }

    class Meta:
        model = models.PotwierdzenieWplaty
        fields = '__all__'


class PotwierdzenieZwrotuSerializer(serializers.ModelSerializer):
    included_serializers = {
        'pracownik': 'hotel.serializers.PracownikSerializer',
        'rezerwacja': 'hotel.serializers.RezerwacjeApartamentowSerializer',
    }

    class Meta:
        model = models.PotwierdzenieZwrotu
        fields = '__all__'


class ProducentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Producent
        fields = '__all__'


class RodzajSprzetuSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RodzajSprzetu
        fields = '__all__'


class OpisSprzetuSerializer(serializers.ModelSerializer):
    included_serializers = {
        'rodzaj': 'hotel.serializers.RodzajSprzetuSerializer',
        'producent': 'hotel.serializers.ProducentSerializer',
    }

    class Meta:
        model = models.OpisSprzetu
        fields = '__all__'


class SprzetSerializer(serializers.ModelSerializer):
    included_serializers = {
        'opis': 'hotel.serializers.OpisSprzetuSerializer',
    }

    class Meta:
        model = models.Sprzet
        fields = '__all__'
