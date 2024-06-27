from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
from django.views.generic.list import ListView
from .forms import *
import re
from collections import Counter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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
    

@login_required
def my_reservations(request):
    user = get_object_or_404(User, pk=request.user.pk)
    ctx = { 
        "upcoming_res" : user.reservations.filter(screening__date__gte=timezone.now()).order_by('screening__date'),
        "old_res" : user.reservations.filter(screening__date__lt=timezone.now()).order_by('-screening__date'),
    }
    return render(request, template_name="movies/my_reservations.html", context=ctx)


class MovieListView(ListView):
    model = Movie
    template_name = "movies/movie_list.html"
    title = "Movie List"
    header = title


class UpcomingMoviesView(MovieListView):
    title = "Upcoming Movies"
    header = title
    
    def get_queryset(self) -> QuerySet[Any]:
        return Movie.get_upcoming_movies()
    
    
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data.get("search_string")
            search_where = form.cleaned_data.get("search_where")
            sort = form.cleaned_data.get("sort_by_score")
            return redirect("movies:searchresults", search_string, search_where, sort)
    else:
        form = SearchForm()
        
    return render(request, template_name="movies/search.html", context={ "form": form })

class SearchResultsView(MovieListView):
    title = "Search Results"
    header = title
    
    def get_queryset(self) -> QuerySet[Any]:
        search_string = self.request.resolver_match.kwargs["search_string"] 
        search_where = self.request.resolver_match.kwargs["search_where"]
        sort = self.request.resolver_match.kwargs["sorted"]
        if search_where == "Title":
            q = self.model.objects.filter(title__icontains=search_string)
        elif search_where == "Director":
            q = self.model.objects.filter(director__icontains=search_string)
        else:
            results = []
            for t in re.findall(r'\w+', search_string):
                results.extend(self.model.objects.filter(tags__name__icontains=t))
            
            c = Counter(results)
            q = []
            
            for m in c:
                i = 0
                m_score = 0 if m.get_score() == None else m.get_score()
                for m2 in q:
                    m2_score = 0 if m2.get_score() == None else m2.get_score()
                    if c[m] > c[m2] or (sort == "True" and c[m] == c[m2] and m_score >= m2_score):
                        break
                    i += 1
                q.insert(i, m)
                
        if sort == "True" and search_where != "Tags":
            q = sorted(q, key=lambda m : 0 if m.get_score() == None else m.get_score(), reverse=True)
            
        return q
    

@login_required
def make_reservation(request, pk):
    if request.method == "POST":
        print(f"Received {request.body}")
        return HttpResponse("")
    return render(request, template_name="movies/make_reservation.html")


def get_screening_seats(request, pk):
    s = get_object_or_404(MovieScreening, pk=pk)
    print(f"requesting seats of {pk}")
    info = {
        "seats": s.seats,
        "rows": s.room.seat_rows,
        "cols": s.room.seat_cols
    }
    return HttpResponse(json.dumps(info))