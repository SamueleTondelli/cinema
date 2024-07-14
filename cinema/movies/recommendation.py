from .models import *


def get_user_movies(user: User):
    return Movie.objects.filter(screenings__reservations__user=user)


def get_user_tagv(user: User):
    m_watch = get_user_movies(user)
    tagv = { t.name : 0 for t in Tag.objects.all() }

    for m in m_watch:
        for t in m.tags.all():
            tagv[t.name] += 1

    return tagv


def get_nmost_similar(user: User, n=None):
    u_tagv = get_user_tagv(user)
    user_mag = 0
    # compute the magnitude of the user tagv
    for t in u_tagv:
        user_mag += u_tagv[t] * u_tagv[t]

    if user_mag == 0:
        return []

    user_mag_sqrt = sqrt(user_mag)

    # get all of the other user which have at least watched one movie
    other_users = list(User.objects.exclude(id=user.id))
    other_users = [u for u in other_users if len(Reservation.objects.filter(user=u)) > 0]

    users_tags = { u:get_user_tagv(u) for u in other_users }
    # compute the cosine similarity
    res = [] # list of tuples (user, cos_similarity)
    for u in users_tags:
        dot_prod = 0
        mag = 0
        tv = users_tags[u]
        for t in tv:
            dot_prod += u_tagv[t] * tv[t]
            mag += tv[t] * tv[t]
        res.append((u, dot_prod/(sqrt(mag)*user_mag_sqrt)))

    # sort by descending similarity
    res.sort(key=lambda ut: ut[1], reverse=True)
    if n != None:
        res = res[:n]
    return res


def get_recommended_movies(user: User, n):
    sim_us = get_nmost_similar(user, 20)
    us_movies = (get_user_movies(user))
    upcoming = Movie.get_upcoming_movies()
    rec_dict = {}
    for u in sim_us:
        # upcoming movies seen by u and not by user
        movies = set(get_user_movies(u[0])).difference(us_movies).intersection(upcoming)
        for m in movies:
            if m in rec_dict:
                rec_dict[m] += u[1]
            else:
                rec_dict[m] = u[1]
        if len(rec_dict) >= n:
            break

    rec = [ (m, rec_dict[m]) for m in rec_dict ]
    rec.sort(key=lambda rm: rm[1], reverse=True)
    rec = [ r[0] for r in rec ]

    if len(rec) < n:
        # fill the result with the highest rated remaining movies
        all_movies = set(upcoming).difference(us_movies).difference(set(rec))
        fill_movies = sorted(list(all_movies), key=lambda m: m.get_score() if m.get_score() != None else 0 , reverse=True)[:n - len(rec)]
        rec += fill_movies
    return rec
