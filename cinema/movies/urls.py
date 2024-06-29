from django.urls import path
from .views import *


app_name = "movies"

urlpatterns = [
    path("infomovie/<pk>/", MovieDetailView.as_view(), name="infomovie"),
    path("myreservations/", my_reservations, name="myreservations"),
    path("upcomingmovies/", UpcomingMoviesView.as_view(), name="upcomingmovies"),
    path("movielist/", MovieListView.as_view(), name="movielist"),
    path("search/", search, name="search"),
    path("search/<str:search_string>/<str:search_where>/<str:sorted>/", SearchResultsView.as_view(), name="searchresults"),
    path("makereservation/<pk>/", make_reservation, name="makereservation"),
    path("screeningseats/<pk>/", get_screening_seats, name="screeningseats"),
    path("cancelres/<pk>/", cancel_res, name="cancelres"),
    path("leavereview/<pk>/", leave_review, name="leavereview"),
    path("myreviews/", MyReviewsView.as_view(), name="myreviews"),
    path("deletereview/<pk>/", delete_review, name="deletereview"),
    path("managermenu/", manager_menu, name="managermenu"),
    path("addmovie/", AddMovieView.as_view(), name="addmovie"),
    path("addscreening/", AddScreeningView.as_view(), name="addscreening"),
    path("addroom/", AddRoomView.as_view(), name="addroom"),
    path("cancelscreenings/", CancelScreeningsView.as_view(), name="cancelscreenings"),
    path("deletescreening/<pk>/", delete_screening, name="deletescreening"),
    path("removemovies/", RemoveMoviesView.as_view(), name="removemovies"),
    path("deletemovie/<pk>/", delete_movie, name="deletemovie"),
    path("removerooms/", RemoveRoomsView.as_view(), name="removerooms"),
    path("deleteroom/<pk>/", delete_room, name="deleteroom")
]