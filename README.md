# Projekt z kursu Bazy Danych 2


## Environment setup
- Install Python 3
- `pip install pipenv`
- `pipenv install`
- `pipenv shell`
- `python app/manage.py runserver`
- Visit API root http://127.0.0.1:8000/api/v1/

## Example API requests
- http://127.0.0.1:8000/api/v1/Klient/?fields[Klient]=imie
- http://127.0.0.1:8000/api/v1/Klient/?filter[imie]=Bilbo
- http://127.0.0.1:8000/api/v1/Klient/?filter[imie]=Bilbo&include=dane_logowania

## Django commands
- Make migrations: `python app/manage.py makemigrations`
- Migrate: `python app/manage.py migrate`
- Run server: `python app/manage.py runserver`

## Links
- Admin interface: http://127.0.0.1:8000/admin/
- API root: http://127.0.0.1:8000/api/v1/
