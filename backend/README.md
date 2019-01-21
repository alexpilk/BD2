# Projekt z kursu Bazy Danych 2


## Environment setup
- Install Python 3
- `pip install pipenv`
- `pipenv install`


## Run using convenience script on Windows:
- `start.bat`


## Run using pipenv
- `pipenv shell`
- `python app/manage.py runserver`

Or:
- `pipenv run python app/manage.py runserver`


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
