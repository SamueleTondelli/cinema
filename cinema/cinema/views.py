from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from movies.models import *
from movies.recommendation import get_recommended_movies


HOMEPAGE_MAX_MOVIES = 5
def home(request):
    movies = Movie.get_upcoming_movies()
    ctx = {
        "movies": movies[:HOMEPAGE_MAX_MOVIES],
        "see_more": len(movies) > HOMEPAGE_MAX_MOVIES,
        "recommended": None
    }
    if request.user.is_authenticated:
        rec = get_recommended_movies(request.user, HOMEPAGE_MAX_MOVIES)
        ctx["recommended"] = rec if len(rec) > 0 else None
        
    return render(request, template_name="home.html", context=ctx)


class CreateUserView(CreateView):
    form_class = NewUserClient
    template_name = "user_create.html"
    success_url = reverse_lazy("login")
    
    
class CreateManagerView(PermissionRequiredMixin, CreateUserView):
    permission_required = "is_staff"
    form_class = NewUserManager