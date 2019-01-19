from rest_framework_json_api import serializers
from . import models


class HotelSerializer(serializers.ModelSerializer):

    verbose_name = serializers.ReadOnlyField(source='__str__')


class DaneLogowaniaSerializer(HotelSerializer):

    class Meta:
        model = models.DaneLogowania
        fields = '__all__'


class KlientSerializer(HotelSerializer):
    included_serializers = {
        'dane_logowania': 'hotel.serializers.DaneLogowaniaSerializer',
    }

    class Meta:
        model = models.Klient
        fields = '__all__'


class PracownikSerializer(HotelSerializer):
    included_serializers = {
        'dane_logowania': 'hotel.serializers.DaneLogowaniaSerializer',
        'stanowisko': 'hotel.serializers.StanowiskoSerializer',
    }

    class Meta:
        model = models.Pracownik
        fields = '__all__'


class BonPracowniczySerializer(HotelSerializer):
    included_serializers = {
        'typ': 'hotel.serializers.TypBonuPracowniczegoSerializer',
        'stanowisko': 'hotel.serializers.StanowiskoSerializer',
    }

    class Meta:
        model = models.BonPracowniczy
        fields = '__all__'


class TypBonuPracowniczegoSerializer(HotelSerializer):

    class Meta:
        model = models.TypBonuPracowniczego
        fields = '__all__'


class StanowiskoSerializer(HotelSerializer):

    class Meta:
        model = models.Stanowisko
        fields = '__all__'


class ApartamentSerializer(HotelSerializer):
    included_serializers = {
        'opis': 'hotel.serializers.OpisApartamentuSerializer',
    }

    class Meta:
        model = models.Apartament
        fields = '__all__'


class OpisApartamentuSerializer(HotelSerializer):
    included_serializers = {
        'rodzaj': 'hotel.serializers.RodzajApartamentuSerializer',
        'lokalizacja': 'hotel.serializers.LokalizacjaSerializer',
    }

    class Meta:
        model = models.OpisApartamentu
        fields = '__all__'


class LokalizacjaSerializer(HotelSerializer):

    class Meta:
        model = models.Lokalizacja
        fields = '__all__'


class RodzajApartamentuSerializer(HotelSerializer):

    class Meta:
        model = models.RodzajApartamentu
        fields = '__all__'


class RabatSerializer(HotelSerializer):
    included_serializers = {
        'klient': 'hotel.serializers.KlientSerializer',
        'typ': 'hotel.serializers.TypRabatuSerializer',
    }

    class Meta:
        model = models.Rabat
        fields = '__all__'


class TypRabatuSerializer(HotelSerializer):

    class Meta:
        model = models.TypRabatu
        fields = '__all__'


class RezerwacjaSprzetuSerializer(HotelSerializer):
    included_serializers = {
        'klient': 'hotel.serializers.KlientSerializer',
        'sprzet': 'hotel.serializers.SprzetSerializer',
    }

    class Meta:
        model = models.RezerwacjaSprzetu
        fields = '__all__'


class RezerwacjeApartamentowSerializer(HotelSerializer):
    included_serializers = {
        'klient': 'hotel.serializers.KlientSerializer',
        'apartament': 'hotel.serializers.ApartamentSerializer',
    }

    class Meta:
        model = models.RezerwacjeApartamentow
        fields = '__all__'


class PotwierdzenieWplatySerializer(HotelSerializer):
    included_serializers = {
        'rezerwacja': 'hotel.serializers.RezerwacjeApartamentowSerializer',
    }

    class Meta:
        model = models.PotwierdzenieWplaty
        fields = '__all__'


class PotwierdzenieZwrotuSerializer(HotelSerializer):
    included_serializers = {
        'pracownik': 'hotel.serializers.PracownikSerializer',
        'rezerwacja': 'hotel.serializers.RezerwacjeApartamentowSerializer',
    }

    class Meta:
        model = models.PotwierdzenieZwrotu
        fields = '__all__'


class ProducentSerializer(HotelSerializer):

    class Meta:
        model = models.Producent
        fields = '__all__'


class RodzajSprzetuSerializer(HotelSerializer):

    class Meta:
        model = models.RodzajSprzetu
        fields = '__all__'


class OpisSprzetuSerializer(HotelSerializer):
    included_serializers = {
        'rodzaj': 'hotel.serializers.RodzajSprzetuSerializer',
        'producent': 'hotel.serializers.ProducentSerializer',
    }

    class Meta:
        model = models.OpisSprzetu
        fields = '__all__'


class SprzetSerializer(HotelSerializer):
    included_serializers = {
        'opis': 'hotel.serializers.OpisSprzetuSerializer',
    }

    class Meta:
        model = models.Sprzet
        fields = '__all__'
