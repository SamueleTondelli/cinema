from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from movies.models import *


HOMEPAGE_MAX_MOVIES = 5
def home(request):
    movies = Movie.objects.all()
    ctx = {
        "movies": movies[:HOMEPAGE_MAX_MOVIES],
        "see_more": len(movies) > HOMEPAGE_MAX_MOVIES
    }
    return render(request, template_name="home.html", context=ctx)


class CreateUserView(CreateView):
    form_class = NewUserClient
    template_name = "user_create.html"
    success_url = reverse_lazy("login")
    
    
class CreateManagerView(PermissionRequiredMixin, CreateUserView):
    permission_required = "is_staff"
    form_class = NewUserManager