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
- ```init_db()```, adds example entries to the database, **warning**: it will try to use certain users which are created only when there's at most 1 user (the superuser)
