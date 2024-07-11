from django.test import TestCase
from .models import *


class MovieScreeningTests(TestCase):
    def test_init_seats(self):
        r = CinemaRoom(name="R", seat_rows=5, seat_cols=10)
        s = MovieScreening()
        s.room = r
        s.init_seats()
        seats = {
            "A": [None] * 10,
            "B": [None] * 10,
            "C": [None] * 10,
            "D": [None] * 10,
            "E": [None] * 10,
        }
        self.assertEqual(s.seats, seats)

    def test_set_reservation(self):
        r = CinemaRoom(name="R", seat_rows=5, seat_cols=5)
        s = MovieScreening()
        s.room = r
        s.init_seats()

        s.set_reservation("A", 0, 2, 1)
        seats = {
            "A": [1, 1, None, None, None],
            "B": [None] * 5,
            "C": [None] * 5,
            "D": [None] * 5,
            "E": [None] * 5,
        }
        self.assertEqual(s.seats, seats)
        self.assertRaises(Exception, s.set_reservation, "F", 0, 1, 2)
        self.assertRaises(Exception, s.set_reservation, "A", 1, 2, 3)
        self.assertRaises(Exception, s.set_reservation, "B", 2, 7, 4)
        s.set_reservation("B", 3, 1, 5)
        seats["B"] = [None, None, None, 5, None]
        self.assertEqual(s.seats, seats)

    def test_remove_reservation(self):
        r = CinemaRoom(name="R", seat_rows=5, seat_cols=5)
        s = MovieScreening()
        s.room = r
        s.init_seats()
        s.set_reservation("A", 0, 2, 1)
        s.set_reservation("B", 3, 1, 2)
        s.remove_reservation(1)
        seats = {
            "A": [None] * 5,
            "B": [None, None, None, 2, None],
            "C": [None] * 5,
            "D": [None] * 5,
            "E": [None] * 5,
        }
        self.assertEqual(s.seats, seats)

    def test_get_free_seats(self):
        r = CinemaRoom(name="R", seat_rows=5, seat_cols=5)
        s = MovieScreening()
        s.room = r
        s.init_seats()
        self.assertEqual(s.get_free_seats(), 5*5)
        s.set_reservation("A", 0, 2, 1)
        self.assertEqual(s.get_free_seats(), 5*5 - 2)
        s.set_reservation("B", 3, 1, 2)
        self.assertEqual(s.get_free_seats(), 5*5 - 2 - 1)
