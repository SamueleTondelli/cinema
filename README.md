# Cinema

This is a django webapp for managing a cinema, made for the final exam of "Tecnologie Web" at UniMoRe.

## Installation
Clone the repository and make sure to have pipenv installed, then:

Activate the virtual enviroment
```
pipenv shell
```

Install dependencies
```
pipenv install
```

Create the superuser:
```
cd cinema
python manage.py createsuperuser
```

Then run the server!
```
python3 manage.py runserver
```

The database can also be initialized by running the ```initcmds.py``` script, note that before the initialization **the database will be deleted**
```
python3 ./initcmds.py
```
