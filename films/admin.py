from django.contrib import admin, messages
from django.db.models import QuerySet

from .models import Movie, Director, Actor, DressingRoom

admin.site.register(Director)
admin.site.register(Actor)


@admin.register(DressingRoom)  # вместо строки сверху admin.site.register(DressingRoom)
class DressingRoomAdmin(admin.ModelAdmin):
    list_display = ['floor', 'number', 'actor']


class RatingFilter(admin.SimpleListFilter):
    title = 'Filter by rating'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [('below 40', 'Low'),
                ('from 40 to 59', 'Average'),
                ('from 60 to 84', 'High'),
                ('85 and above', 'The Highest')
                ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'below 40':
            return queryset.filter(rating__lt=40)
        if self.value() == 'from 40 to 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        if self.value() == 'from 60 to 84':
            return queryset.filter(rating__gte=60).filter(rating__lt=85)
        if self.value() == '85 and above':
            return queryset.filter(rating__gte=85)
        return queryset


@admin.register(Movie)  # вместо строки  admin.site.register(Movie, MovieAdmin)
class MovieAdmin(admin.ModelAdmin):
    # поля записи модели(каждого фильма), исключаемые из формы её редактирования:
    # exclude = ['slug']
    # недоступные для редактирования поля:
    readonly_fields = ['year']
    prepopulated_fields = {'slug': ('name',)}
    # список дополнительных колонок, которые хочется добавить:
    list_display = ['name', 'rating', 'director', 'budget', 'currency', 'rating_status']
    # список колонок, поддерживающих редактирование записей:
    list_editable = ['rating', 'director', 'budget', 'currency']
    # первое поле 'name' ─ ссылка на объект, её нельзя давать редактировать!
    filter_horizontal = ['actors']  # или filter_vertical
    # сортировка по убыванию рейтинга (в первую очередь) и по возрастанию бюджета:
    ordering = ['-rating', 'budget']
    # пагинация (пейджинг) - количество отображаемых на одной странице фильмов:
    list_per_page = 10
    actions = ['set_dollars', 'set_euros']
    search_fields = ['name__startswith']  # поисковая строка по началу имени
    list_filter = ['name', 'currency', RatingFilter]

    # вычисляемое поле с сортировкой по рейтингу:
    @admin.display(ordering='rating', description='recommendation')
    def rating_status(self, movie: Movie):  # movie - экземпляр класса Movie
        if movie.rating < 40:
            return 'отстой, не смотри!'
        if movie.rating < 55:
            return 'на любителя'
        if movie.rating < 70:
            return 'на один раз'
        if movie.rating < 85:
            return 'можно смотреть'
        return 'обязательно посмотри'

    @admin.action(description='Set Dollars as currency')
    def set_dollars(self, request, qs: QuerySet):
        qs.update(currency=Movie.USD)

    @admin.action(description='Set Euros as currency')
    def set_euros(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.EUR)
        self.message_user(request,
                          f'Было обновлено {count_updated} записей',
                          messages.ERROR)  # предупреждающее(красное) сообщение
