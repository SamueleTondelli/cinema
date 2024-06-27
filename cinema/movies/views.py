from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/info_movie.html"
    
    def get_movie_score(self):
        return self.get_object().get_score()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        
        act_list = ""
        m = self.get_object()
        for a in m.actors:
            act_list += a + ", "
        ctx["actor_list"] = act_list[:-2]
        
        tag_list = ""
        for t in m.tags.all():
            tag_list += t.name + ", "
        ctx["tag_list"] = tag_list[:-2]
        
        return ctx
    

@login_required
def my_reservations(request):
    user = get_object_or_404(User, pk=request.user.pk)
    ctx = { 
        "upcoming_res" : user.reservations.filter(screening__date__gte=timezone.now()).order_by('screening__date'),
        "old_res" : user.reservations.filter(screening__date__lt=timezone.now()).order_by('-screening__date'),
    }
    return render(request, template_name="movies/my_reservations.html", context=ctx)