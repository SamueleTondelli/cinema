from django.urls import path
from .views import *


app_name = "movies"

urlpatterns = [
    path("infomovie/<pk>/", MovieDetailView.as_view(), name="infomovie"),
    path("myreservations/", my_reservations, name="myreservations"),
    path("upcomingmovies/", UpcomingMoviesView.as_view(), name="upcomingmovies"),
    path("search/", search, name="search"),
    path("search/<str:search_string>/<str:search_where>/<str:sorted>/", SearchResultsView.as_view(), name="searchresults"),
    path("makereservation/<pk>/", make_reservation, name="makereservation"),
    path("screeningseats/<pk>/", get_screening_seats, name="screeningseats"),
    path("cancelres/<pk>/", cancel_res, name="cancelres")
]