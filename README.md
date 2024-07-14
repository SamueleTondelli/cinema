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

Migrate the database:
```
cd cinema
python3 manage.py migrate
```

Create the superuser:
```
python3 manage.py createsuperuser
```

Then run the server!
```
python3 manage.py runserver
```

## Database initialization
For the app to correctly work, it needs the right groups (Clients and Managers) with the right permissions, they can either be created from the admin page or with the helper function ```init_groups()``` in ```cinema/initcmds.py``` added to the file ```cinema/urls.py```.
There's also the possibility to initialize the database with example values, using two other helper function in ```cinema/initcmds.py```:
- ```erase_db()```, erases the database (but keeps the users), suggested before using the next function to avoid conflicts
- ```init_db()```, adds example entries to the database, **warning**: it will try to use certain users which are created only when there's at most 1 user (the superuser), so it's suggested to use this utility only when the database is completely empty to test the app

## Tests
There is a suite of tests, to run them:
```
python3 manage.py test movies
```

They test:
- that the reservation logic works correctly and avoids conflicts
- that movies showed as "upcoming" are actually upcoming
- that only managers and the admin can access the manager menu

## Dependencies
All of the dependencies are contained in the ```Pipfile``` file, in particular:
- ```django``` is used as the backend framework
- ```django-crispy-forms``` and ```crispy-bootstrap4``` are necessary to use django crispy forms
- ```django-braces``` is used for the GroupRequiredMixin to make certain CBV only accessible to certain groups
- ```pillow``` is used to handle images
