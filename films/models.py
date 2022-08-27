from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
# from django.utils.text import slugify


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    director_email = models.EmailField()

    def get_url(self):
        return reverse('director_detail', args=[self.last_name])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class DressingRoom(models.Model):
    floor = models.IntegerField()
    number = models.IntegerField()

    def str(self):
        return f'{self.floor} {self.number}'


class Actor(models.Model):
    MALE, FEMALE = 'M', 'F'
    GENDERS = [(MALE, 'Man'), (FEMALE, 'Woman')]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dressing = models.OneToOneField(DressingRoom, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default=MALE)

    def get_url(self):
        return reverse('actor_detail', args=[self.last_name])

    def __str__(self):
        if self.gender == self.MALE:
            return f'actor {self.first_name} {self.last_name}'
        else:
            return f'actress {self.first_name} {self.last_name}'


class Movie(models.Model):
    EUR, USD, UAH = 'EUR', 'USD', 'UAH'
    CURRENCY_CHOICES = [(EUR, 'Euros'), (USD, 'Dollars'), (UAH, 'Hryvnias')]
    name = models.CharField(max_length=40)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    # blank=True (можно не заполнить, оставить пустым) делает поле необязательным:
    year = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(default=1000000, blank=True, validators=[MinValueValidator(1)])
    # выбор значения из ограниченного списка вариантов:
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=USD)
    slug = models.SlugField(default='', null=False, db_index=True)
    # внешний ключ (related_name - псевдоним поля, по которому из director получают список всех его фильмов):
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True, related_name='movies')
    # PROTECT не даст удалить режиссёра при наличии связанных с ним фильмов
    # CASCADE при удалении режиссёра предложит удалить все связанные с ним фильмы
    # SET_NULL при удалении режиссёра в связанных с ним фильмах проставит null
    # SET_DEFAULT при удалении режиссёра в -//- фильмах проставит значение по умолчанию
    actors = models.ManyToManyField(Actor, related_name='movies')  # связь с таблицей Actor
    '''
    # не надо, т.к. slug сохраняется с помощью атрибута prepopulated_fields класса MovieAdm в admin.py
    def save(self, *args, **kwargs):  # переопределение метода save родит. класса Model
        self.slug = slugify(self.name)  # в имени экземпляра пробелы заменяет дефисами
        super(Movie, self).save(*args, **kwargs)  # вызов метода save у родителя
    '''

    def get_url(self):
        return reverse('film_detail', args=[self.slug])

    def __str__(self):
        return f'{self.name} ─ {self.rating}%'

# python manage.py makemigrations
# python manage.py migrate
