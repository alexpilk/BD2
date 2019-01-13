import logging

from app.api import api

logging.basicConfig(level=logging.DEBUG)

dane_logowania = api.create(
    'DaneLogowania',
    attributes={
        "login": "JanPawel",
        "email": "jan@op.pl",
        "haslo": "druuugi"
    }
)

klient = api.create(
    'Klient',
    attributes=
    {
        "imie": "Jan",
        "nazwisko": "Pawel",
        "adres": "pl. Jana Pawla",
        "numer_karty": "0000 0000 0000 0001"
    },
    relationships={
        'dane_logowania': {
            'type': 'DaneLogowania',
            'id': 'JanPawel'
        }
    })

api.update(
    'Klient',
    attributes=
    {
        "imie": klient['imie'],
        "nazwisko": "inne nazwisko",
        "adres": klient['adres'],
        "numer_karty": klient['numer_karty']
    },
    relationships={
        'dane_logowania': {
            'type': 'DaneLogowania',
            'id': klient['dane_logowania']['id']
        }
    },
    _id=klient['id'])

klient_z_danymi_logowania = api.get(
    'Klient',
    filters={
        'id': klient['id']
    },
    include=[
        'dane_logowania'
    ]
)
api.delete('Klient', _id=klient['id'])
api.delete('DaneLogowania', _id=dane_logowania['id'])
