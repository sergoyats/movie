from django.urls import path

from . import views

urlpatterns = [
    path('', views.show_all_films),
    path('film/<slug:slug_film>', views.show_one_film, name='film_detail'),
    path('directors', views.show_all_directors),
    path('directors/<str:director_name>', views.show_one_director, name='director_detail'),
    path('actors', views.show_all_actors),
    path('actors/<str:actor_name>', views.show_one_actor, name='actor_detail'),
]
