from django.urls import path
from .views import *


app_name = "movies"

urlpatterns = [
    path("infomovie/<pk>/", MovieDetailView.as_view(), name="infomovie"),
    path("myreservations/", my_reservations, name="myreservations"),
    path("upcomingmovies/", UpcomingMoviesView.as_view(), name="upcomingmovies")
]