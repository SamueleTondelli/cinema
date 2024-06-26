from movies.models import *
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone


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
    
    tags = ["Action", "Horror", "Romantic", "Adventure", "Fantasy", "Military", "Comedy"]
    
    for st in tags:
        t = Tag()
        t.name = st
        t.save()
        
    movies = {
        "All" : {"director": "all dir", "actors": ["Tipo con nome bello lungo", "act1", "act2", "act3", "act4", "act4", "act5", "act6", "act7", "act8", "act9", "act10"], "duration": timedelta(minutes=120), "tags": tags},
        "ActHorr" : {"director": "acthorr dir", "actors": ["act1", "act2"], "duration": timedelta(minutes=120), "tags": tags[0:2]},
        "RomAdv" : {"director": "romadv dir", "actors": ["act1", "act3"], "duration": timedelta(minutes=150), "tags": tags[2:4]},
        "FantMil" : {"director": "fantmil dir", "actors": ["act6", "act7"], "duration": timedelta(minutes=90), "tags": tags[4:6]},
        "ActHorr 2" : {"director": "acthorr dir", "actors": ["act1", "act2"], "duration": timedelta(minutes=120), "tags": tags[0:2]},
        "RomAdv 2" : {"director": "romadv dir", "actors": ["act1", "act3"], "duration": timedelta(minutes=150), "tags": tags[2:4]},
        "FantMil 2" : {"director": "fantmil dir", "actors": ["act6", "act7"], "duration": timedelta(minutes=90), "tags": tags[4:6]},
        "ActHorr 3" : {"director": "acthorr dir", "actors": ["act1", "act2"], "duration": timedelta(minutes=120), "tags": tags[0:2]},
        "RomAdv 3" : {"director": "romadv dir", "actors": ["act1", "act3"], "duration": timedelta(minutes=150), "tags": tags[2:4]},
        "FantMil 3" : {"director": "fantmil dir", "actors": ["act6", "act7"], "duration": timedelta(minutes=90), "tags": tags[4:6]},
    }
    
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
    }
    
    for k in rooms:
        r = CinemaRoom()
        e = rooms.get(k)
        r.name = k
        r.seat_rows = e["r"]
        r.seat_cols = e["c"]
        r.save()
    
    if len(User.objects.all()) == 1:
        print("Creating users")
        for i in range(1,5):
            u = User.objects.create_user(username="user"+str(i), password="samplepw1!")
            u.save()
    
    today = timezone.now()
    screenings = [
        { "room": CinemaRoom.objects.filter(name__exact="R1")[0], "movie": Movie.objects.filter(title__exact="ActHorr")[0], "date": today + timedelta(1) },
        { "room": CinemaRoom.objects.filter(name__exact="R2")[0], "movie": Movie.objects.filter(title__exact="ActHorr")[0], "date": today + timedelta(2) },
        { "room": CinemaRoom.objects.filter(name__exact="R3")[0], "movie": Movie.objects.filter(title__exact="RomAdv")[0], "date": today + timedelta(3) },
        { "room": CinemaRoom.objects.filter(name__exact="R3")[0], "movie": Movie.objects.filter(title__exact="FantMil")[0], "date": today + timedelta(4) },
    ]
    
    m_screenings = []
    for sc in screenings:
        s = MovieScreening()
        s.room = sc["room"]
        s.movie = sc["movie"]
        s.date = sc["date"]
        s.init_seats()
        s.save()
        m_screenings.append(s)
    
    reservations = [
        {"s": 0, "user": "user1", "seats_args": ("A",4,2)},
        {"s": 0, "user": "user2", "seats_args": ("B",4,5)},
        {"s": 1, "user": "user3", "seats_args": ("C",2,1)},
        {"s": 2, "user": "user4", "seats_args": ("D",1,6)},
        {"s": 3, "user": "user4", "seats_args": ("E",0,1)},
    ]
    
    for sr in reservations:
        r = Reservation()
        r.screening = m_screenings[sr["s"]]
        r.user = User.objects.filter(username__exact=sr["user"])[0]
        seats = sr["seats_args"]
        r.save()
        r.set_seats(seats[0], seats[1], seats[2])
        r.save()
        
    reviews = [
        {"user": "user1", "movie": Movie.objects.filter(title__exact="All")[0], "score": 6, "text": "iouwegeifgwaibibwibviw<kebviuwabvkjbsd<ibviubeivbsiuvhbwibskvdjvbwasuvbakljv"},
        {"user": "user2", "movie": Movie.objects.filter(title__exact="All")[0], "score": 8, "text": "iouwegeifgwaibibwibviw<kebviuwab a sfafs asfma lkl kfa sflkaò fmlkam flkam lkfaslk "},
        {"user": "user3", "movie": Movie.objects.filter(title__exact="All")[0], "score": 5, "text": "oeiqjho wj weoijwo oiwj goiwj goiwrg oiwoig jwoigw jibviubeivbsiuvhbwibskvdjvbwasuvbakljv"},
        {"user": "user4", "movie": Movie.objects.filter(title__exact="All")[0], "score": 9, "text": "iwethiuwhe iuw euiwiue hui whiuwefh uiwefh uihwef iuh iu ehwiuefh iuhe iu"},
        {"user": "user1", "movie": Movie.objects.filter(title__exact="ActHorr")[0], "score": 5, "text": "iwethiuwhe iuw erterg ehwiuefh iuhe iu"},
    ]
    
    for sr in reviews:
        r = Review()
        r.user = User.objects.filter(username__exact=sr["user"])[0]
        r.movie = sr["movie"]
        r.score = sr["score"]
        r.text = sr["text"]
        r.save()
    
    print("Dump DB")
    print(Tag.objects.all())
    print(Movie.objects.all())
    print(CinemaRoom.objects.all())
    print(MovieScreening.objects.all())
    print(Reservation.objects.all())
