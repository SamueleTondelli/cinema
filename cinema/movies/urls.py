from django.urls import path
from .views import *


app_name = "movies"

urlpatterns = [
    path("infomovie/<pk>/", MovieDetailView.as_view(), name="infomovie"),
]