from .client import ApiClient


api = ApiClient('http://localhost:8000/api/v1/')


def example():
    klienty = api.get('Klient')
    print(klienty)
