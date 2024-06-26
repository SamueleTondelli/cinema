from typing import Any
from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import *
import json


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