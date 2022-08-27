from django.db.models import F, Max, Min, Avg, Count, Value
from django.shortcuts import render, get_object_or_404

from .models import Movie, Director, Actor


def show_all_films(request):
    # the F object  is allowing to access other columns inside an ORM query
    # sort by ascending year of release (first of all) and descending rating:
    # films = Movie.objects.order_by(F('year').asc(nulls_last=True), '-rating')
    # adding a new field in ORM query:
    films = Movie.objects.annotate(true_bool=Value(True),
                                   false_bool=Value(False),
                                   str_field=Value('Hello'),
                                   int_field=Value(123),
                                   new_budget=F('budget') + 100,
                                   product=F('rating') * F('year'),
                                   ).order_by(F('year'), '-rating')
    agg = films.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))
    return render(request, 'films/all_films.html', {
        'films': films,
        'agg': agg,
    })


def show_one_film(request, slug_film: str):
    film = get_object_or_404(Movie, slug=slug_film)
    return render(request, 'films/one_film.html', {
        'film': film,
    })


def show_all_directors(request):
    directors = Director.objects.all()
    return render(request, 'films/all_directors.html', {
        'directors': directors,
    })


def show_one_director(request, director_name: str):
    director = get_object_or_404(Director, last_name=director_name)
    return render(request, 'films/one_director.html', {
        'director': director,
    })


def show_all_actors(request):
    actors = Actor.objects.order_by(F('last_name'))
    return render(request, 'films/all_actors.html', {
        'actors': actors,
    })


def show_one_actor(request, actor_name: str):
    actor = get_object_or_404(Actor, last_name=actor_name)
    return render(request, 'films/one_actor.html', {
        'actor': actor,
    })
