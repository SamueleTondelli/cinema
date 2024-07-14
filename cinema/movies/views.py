from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.utils import timezone
from django.views.generic.list import ListView
from .forms import *
import re
from collections import Counter
from django.urls import reverse, reverse_lazy
import json
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView
from braces.views import GroupRequiredMixin


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

    def can_user_review(self):
        if self.request.user.is_authenticated:
            return self.get_object().can_user_review(self.request.user.id)
        return False


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
    s = get_object_or_404(MovieScreening, pk=pk)
    if s.date < timezone.now():
        return HttpResponseNotFound("")
    if request.method == "POST":
        #print(f"Received {request.body}")
        ress = Reservation.objects.filter(user=request.user,screening=s)
        if len(ress) > 0:
            r = ress[0]
            s = r.screening
            s.remove_reservation(r.id)
            r.seats = []
        else:
            r = Reservation()
            r.user = request.user
            r.screening = s
            r.save()

        resp = json.loads(request.body)
        try:
            for seat in resp["reserving_seats"]:
                r.set_seat_from_idx(int(seat))
            r.save()
            s.save()
        except Exception as e:
            print(e)
            r.delete()
            return HttpResponse(reverse("movies:myreservations") + "?makeres=err")
        return HttpResponse(reverse("movies:myreservations") + "?makeres=ok")
    return render(request, template_name="movies/make_reservation.html", context={"screening": s})


@login_required
def get_screening_seats(request, pk):
    s = get_object_or_404(MovieScreening, pk=pk)
    user = request.user
    r = Reservation.objects.filter(user=user,screening=s)
    #print(f"requesting seats of {pk}")
    info = {
        "seats": s.seats,
        "rows": s.room.seat_rows,
        "cols": s.room.seat_cols
    }
    if (len(r) > 0):
        info["res_id"] = r[0].id
    return HttpResponse(json.dumps(info))


@login_required
def cancel_res(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    if res.user != request.user:
        return HttpResponseNotFound("")
    res.screening.remove_reservation(res.id)
    res.screening.save()
    res.delete()
    return redirect("movies:myreservations")


@login_required
def leave_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data.get("score")
            text = form.cleaned_data.get("text")
            r = Review()
            r.movie = movie
            r.user = request.user
            r.score = score
            r.text = text
            r.save()
            return redirect("movies:infomovie", pk)

    form = ReviewForm()
    return render(request, template_name="movies/leave_review.html", context={"movie":movie, "form": form})


class MyReviewsView(LoginRequiredMixin, ListView):
    model = Review
    template_name = "movies/my_reviews.html"

    def get_queryset(self) -> QuerySet[Any]:
        user = User.objects.filter(id=self.request.user.id)[0]
        return Review.objects.filter(user=user)

@login_required
def delete_review(request, pk):
    rev = get_object_or_404(Review, pk=pk)
    if rev.user != request.user:
        return HttpResponseNotFound("")
    rev.delete()
    return redirect("movies:myreviews")


def is_manager(user):
    return user.groups.filter(name="Managers").exists()


@user_passes_test(is_manager)
def manager_menu(request):
    return render(request, template_name="movies/manager_menu.html")


class AddEntryView(CreateView):
    title = "Add Entry"
    template_name = "movies/add_entry.html"


class AddMovieView(GroupRequiredMixin, AddEntryView):
    group_required = ["Managers"]
    title = "Add Movie"
    model = Movie
    form_class = AddMovieForm

    def get_success_url(self):
        return reverse("movies:managermenu") + "?addentry=ok"


class AddScreeningView(GroupRequiredMixin, AddEntryView):
    group_required = ["Managers"]
    title = "Add Screening"
    model = MovieScreening
    form_class = AddScreeningForm

    def get_success_url(self):
        return reverse("movies:managermenu") + "?addentry=ok"


class AddRoomView(GroupRequiredMixin, AddEntryView):
    group_required = ["Managers"]
    title = "Add Room"
    model = CinemaRoom
    form_class = AddRoomForm

    def get_success_url(self):
        return reverse("movies:managermenu") + "?addentry=ok"


class CancelScreeningsView(GroupRequiredMixin, ListView):
    group_required = ["Managers"]
    model = MovieScreening
    template_name = "movies/cancel_screenings.html"

    def get_queryset(self):
        return MovieScreening.objects.filter(date__gte=timezone.now()).order_by("date")


@user_passes_test(is_manager)
def delete_screening(request, pk):
    s = get_object_or_404(MovieScreening, pk=pk)
    s.delete()
    return redirect(reverse("movies:cancelscreenings") + "?delete=ok")


class RemoveMoviesView(GroupRequiredMixin, MovieListView):
    group_required = ["Managers"]
    title = "Delete movies"
    header = title

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["delete_movie"] = "yes"
        return ctx


@user_passes_test(is_manager)
def delete_movie(request, pk):
    m = get_object_or_404(Movie, pk=pk)
    m.delete()
    return redirect(reverse("movies:removemovies") + "?delete=ok")


class RemoveRoomsView(GroupRequiredMixin, ListView):
    group_required = ["Managers"]
    model = CinemaRoom
    template_name = "movies/remove_rooms.html"


@user_passes_test(is_manager)
def delete_room(request, pk):
    r = get_object_or_404(CinemaRoom, pk=pk)
    r.delete()
    return redirect(reverse("movies:removerooms") + "?delete=ok")
