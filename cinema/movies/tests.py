from datetime import timedelta
from django.test import TestCase
from .models import *
from django.urls import reverse
from django.contrib.auth.models import Group


class MovieScreeningTests(TestCase):
    def test_init_seats(self):
        """
        All of the seats of a reservations are correctly initialized to None (free)
        """
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
        """
        Reservations can only be made on free and existing seats
        """
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
        """
        Removing a reservation only frees the seats of said reservation
        """
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
        """
        Number of free seats is correctly calculated and it gets lower when new reservations are made
        """
        r = CinemaRoom(name="R", seat_rows=5, seat_cols=5)
        s = MovieScreening()
        s.room = r
        s.init_seats()
        self.assertEqual(s.get_free_seats(), 5*5)
        s.set_reservation("A", 0, 2, 1)
        self.assertEqual(s.get_free_seats(), 5*5 - 2)
        s.set_reservation("B", 3, 1, 2)
        self.assertEqual(s.get_free_seats(), 5*5 - 2 - 1)


class UpcomingMoviesViewTest(TestCase):
    def test_no_upcoming_movies(self):
        """
        If there are no upcoming movies, the upcomingmovies page should display "There are no movies here"
        """
        response = self.client.get(reverse("movies:upcomingmovies"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no movies here")
        self.assertQuerySetEqual(response.context["object_list"], [])

    def test_upcoming_movies(self):
        """
        The upcomingmovies page should only contain upcoming movies ordered based on the closest screening date
        """
        m1 = Movie(title="m1", duration=timedelta(minutes=120))
        m2 = Movie(title="m2", duration=timedelta(minutes=120))
        m3 = Movie(title="m3", duration=timedelta(minutes=120))
        m4 = Movie(title="m4", duration=timedelta(minutes=120))
        m1.save()
        m2.save()
        m3.save()
        m4.save()

        r = CinemaRoom(name="R", seat_rows=5, seat_cols=5)
        r.save()

        s1 = MovieScreening()
        s1.movie = m1
        s1.date = timezone.now() + timedelta(2)
        s1.room = r
        s1.save()

        s2 = MovieScreening()
        s2.movie = m2
        s2.date = timezone.now() + timedelta(1)
        s2.room = r
        s2.save()

        s3 = MovieScreening()
        s3.movie = m3
        s3.date = timezone.now() + timedelta(3)
        s3.room = r
        s3.save()

        s4 = MovieScreening()
        s4.movie = m4
        s4.date = timezone.now() - timedelta(1)
        s4.room = r
        s4.save()

        response = self.client.get(reverse("movies:upcomingmovies"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "There are no movies here")
        self.assertQuerySetEqual(response.context["object_list"], [m2, m1, m3])


class ManagerMenuViewTest(TestCase):
    def test_not_manager(self):
        """
        Non managers should not be able to access the managermenu page
        """
        response = self.client.get(reverse("movies:managermenu"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?auth=notok&next=/movies/managermenu/")

        u = User.objects.create_user(username="u1", password="samplepw1!")
        u.save()
        g = Group(name="Clients")
        g.save()
        g.user_set.add(u)
        self.client.login(username="u1", password="samplepw1!")
        response = self.client.get(reverse("movies:managermenu"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?auth=notok&next=/movies/managermenu/")

    def test_is_manager(self):
        """
        Managers and the admin should be able to access the managermenu page
        """
        m = User.objects.create_user(username="m1", password="samplepw1!")
        m.save()
        g = Group(name="Managers")
        g.save()
        g.user_set.add(m)
        self.client.login(username="m1", password="samplepw1!")
        response = self.client.get(reverse("movies:managermenu"))
        self.assertEqual(response.status_code, 200)

        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("movies:managermenu"))
        self.assertEqual(response.status_code, 200)
