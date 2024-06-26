from django.contrib import admin
from .models import *

admin.site.register(Movie)
admin.site.register(Tag)
admin.site.register(CinemaRoom)
admin.site.register(MovieScreening)
admin.site.register(Reservation)
admin.site.register(Review)