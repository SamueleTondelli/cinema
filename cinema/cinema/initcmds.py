from movies.models import *
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
import copy
import random
from django.contrib.auth.models import Group


def erase_db():
    print("Deleting database")
    Movie.objects.all().delete()
    Tag.objects.all().delete()
    CinemaRoom.objects.all().delete()
    MovieScreening.objects.all().delete()
    Reservation.objects.all().delete()
    Review.objects.all().delete()


def init_db():
    if len(Movie.objects.all()) > 0:
        return

    tags = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Horror", "Musical", "Mistery", "Romance", "Science Fiction", "Thriller", "Western"]

    for st in tags:
        t = Tag()
        t.name = st
        t.save()

    movies = {}

    for i in range(len(tags)):
        tgs = [tags[i], tags[(i+1) % len(tags)], tags[(i+2) % len(tags)]]
        title = ""
        for t in tgs:
            title += t + " "
        actors = [ "Actor " + str(i+j) for j in range(4) ]
        movies[title] = {
            "title": title,
            "director": title + " director",
            "actors": actors,
            "duration": timedelta(minutes=120),
            "tags": tgs
        }

        title2 = title + " 2"
        movies[title2] = movies[title]
        movies[title2]["title"] = title2

    for k in movies:
        m = Movie()
        e = movies.get(k)
        m.title = k
        m.director = e["director"]
        m.actors = e["actors"]
        m.duration = e["duration"]
        m.save()
        for t in e["tags"]:
            m.tags.add(Tag.objects.filter(name__exact=t)[0].id)
        m.save()

    rooms = {
        "R1" : {"r": 15, "c": 25},
        "R2" : {"r": 8, "c": 15},
        "R3" : {"r": 10, "c": 20},
        "R4" : {"r": 12, "c": 20}
    }

    for k in rooms:
        r = CinemaRoom()
        e = rooms.get(k)
        r.name = k
        r.seat_rows = e["r"]
        r.seat_cols = e["c"]
        r.save()

    if len(User.objects.all()) <= 1:
        print("Creating users")
        for i in range(1,5):
            u = User.objects.create_user(username="user"+str(i), password="samplepw1!")
            g = Group.objects.get(name="Clients")
            g.user_set.add(u)
            u.save()

        m = User.objects.create_user(username="manager1", password="samplepw1!")
        g = Group.objects.get(name="Managers")
        g.user_set.add(m)


    today = timezone.now()
    screenings = []

    i = 1
    d = 1
    for m in Movie.objects.all():
        s = {}
        s["movie"] = m
        s["room"] = CinemaRoom.objects.filter(name__exact="R"+str(i))[0]
        if i >= len(rooms):
            i = 1
            d += 1
        else:
            i += 1
        s["date"] = today + timedelta(d)
        screenings.append(s)
        s = copy.deepcopy(s)
        s["date"] = today - timedelta(d)
        screenings.append(s)


    for sc in screenings:
        s = MovieScreening()
        s.room = sc["room"]
        s.movie = sc["movie"]
        s.date = sc["date"]
        s.init_seats()
        s.save()


    reservations = {
        "user1": {"tags": [Tag.objects.filter(name="Action")[0], Tag.objects.filter(name="Fantasy")[0], Tag.objects.filter(name="Science Fiction")[0]], "row": "A", "start": 3, "count": 2 },
        "user2": {"tags": [Tag.objects.filter(name="Adventure")[0], Tag.objects.filter(name="Comedy")[0], Tag.objects.filter(name="Western")[0]], "row": "B", "start": 1, "count": 3 },
        "user3": {"tags": [Tag.objects.filter(name="Crime")[0], Tag.objects.filter(name="Mistery")[0], Tag.objects.filter(name="Thriller")[0]], "row": "C", "start": 4, "count": 2 },
        "user4": {"tags": [Tag.objects.filter(name="Animation")[0], Tag.objects.filter(name="Musical")[0], Tag.objects.filter(name="Romance")[0]], "row": "D", "start": 0, "count": 2 },
    }

    for sr in reservations:
        ts = reservations[sr]["tags"]
        mvs = set(Movie.objects.filter(tags=ts[0]).exclude(title__contains="2") | Movie.objects.filter(tags=ts[1]).exclude(title__contains="2") | Movie.objects.filter(tags=ts[2]).exclude(title__contains="2"))
        for m in mvs:
            r = Reservation()
            s = MovieScreening.objects.filter(movie=m).filter(date__lt=timezone.now())[0]
            r.user = User.objects.filter(username__exact=sr)[0]
            r.screening = s
            r.save()
            r.set_seats(reservations[sr]["row"], reservations[sr]["start"], reservations[sr]["count"])
            r.save()

    for u in User.objects.all():
        mvs = [m for m in Movie.objects.all() if m.can_user_review(u.id)][2:]
        t = " Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras blandit tristique nisi, nec sodales sapien blandit ut. Integer sed commodo dui."
        for m in mvs:
            r = Review()
            r.user = u
            r.movie = m
            score = random.randint(1, 10)
            r.score = score
            r.text = str(score) + "/10 from " + u.username + t
            r.save()

    print("Finished DB initialization")


def init_groups():
    clients = Group.objects.get_or_create(name="Clients")
    clients.permissions.set(["movies.add_reservation", "movies.change_reservation", "movies.remove_reservation",
                            "movies.add_review", "movies.change_review", "movies.remove_review"])
    managers = Group.objects.get_or_create(name="Managers")
    managers.permissions.set(["movies.add_reservation", "movies.change_reservation", "movies.remove_reservation",
                            "movies.add_review", "movies.change_review", "movies.remove_review",
                            "movies.add_cinemaroom", "movies.change_cinemaroom", "movies.remove_cinemaroom",
                            "movies.add_movie", "movies.change_movie", "movies.remove_movie",
                            "movies.add_moviescreening", "movies.change_moviescreening", "movies.remove_moviescreening",])
