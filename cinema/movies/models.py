from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Tag(models.Model):
    name = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    actors = models.JSONField(default=list)
    duration = models.DurationField()
    tags = models.ManyToManyField(Tag, related_name="movies")
    
    def get_score(self):
        revs = self.reviews.all()
        n = len(revs)
        if n == 0: return None
        s = 0
        for r in revs:
            s += r.score
        return s/n

    def __str__(self):
        return '"' + self.title + '" by "' + self.director + '"'
    

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    score = models.PositiveIntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    text = models.CharField(default="", max_length=300)
    
    def __str__(self):
        return self.user.username + " gave " + self.movie.title + " a " + str(self.score) + "/10"
    
    class Meta:
        unique_together = (('movie', 'user'))
    


class CinemaRoom(models.Model):
    name = models.CharField(max_length=10, unique=True)
    seat_rows = models.IntegerField(default=10)
    seat_cols = models.IntegerField(default=20)
    
    def __str__(self):
        return self.name + " with " + str(self.seat_rows) + "x" + str(self.seat_cols) + " seats"
    
    def get_total_seats(self):
        return self.seat_cols * self.seat_rows
    
    
class MovieScreening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="screenings")
    room = models.ForeignKey(CinemaRoom, on_delete=models.CASCADE, related_name="screenings")
    seats = models.JSONField(default=dict)
    date = models.DateTimeField()
    
    def init_seats(self):
        rows = self.room.seat_rows
        cols = self.room.seat_cols
        s = {}
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for r in range(0, rows):
            s[letters[r]] = [None] * cols
        self.seats = s
        
    def get_seat_reserv(self, row, col, convert_col=False):
        if convert_col:
            col -= 1
            
        if self.seats.get(row) == None or col < 0 or col >= self.room.seat_cols:
            raise Exception("Illegal argument in get_seat_reserv(), got row=" + str(row) + " col=" + str(col))
        return self.seats.get(row)[col]
    
    def set_reservation(self, row, start_col, seats_number, res_id, convert_col=False):
        if convert_col:
            start_col -= 1
        
        for c in range(start_col, start_col + seats_number):
            if self.get_seat_reserv(row, c, False) != None:
                raise Exception("Tried reserving already occupied seats!")
        
        r = self.seats.get(row)
        for c in range(start_col, start_col + seats_number):
            r[c] = res_id
        self.seats[row] = r

    def __str__(self):
        return str(self.movie) + " on the " + str(self.date)
    

class Reservation(models.Model):
    screening = models.ForeignKey(MovieScreening, on_delete=models.CASCADE, related_name="reservations")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    seats = models.JSONField(default=list)
    
    def set_seats(self, row, start_col, seats_number):
        self.screening.set_reservation(row, start_col, seats_number, self.id)
        self.screening.save()
        for c in range(start_col, start_col + seats_number):
            self.seats.append((row, c))
    
    def __str__(self):
        return str(self.screening) + " reserved by " + str(self.user)