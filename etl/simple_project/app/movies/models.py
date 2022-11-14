import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Filmtype(models.TextChoices):
    MOVIE = 'movie', _('movies')
    TV_SHOW = 'tv_show', _('tv_show')


class Filmwork(UUIDMixin, TimeStampedMixin):
    # certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    # Параметр upload_to указывает, в какой подпапке будут храниться загружемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    # file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    type = models.CharField(max_length=10, choices=Filmtype.choices, default=Filmtype.MOVIE)
    genres = models.ManyToManyField('Genre', through='GenreFilmwork')
    persons = models.ManyToManyField('Person', through='PersonFilmwork')
    title = models.TextField(_('title'))
    certificate = models.CharField(_('certificate'), max_length=512, blank=True, null=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    description = models.TextField(_('description'), null=True)
    creation_date = models.DateField(_('creation_date'), auto_now_add=True, null=True)
    rating = models.FloatField(
        _('rating'), null=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('Genre film')
        verbose_name_plural = _('Genres films')
        index_together = [
            ["film_work_id", "genre_id"],
        ]


class Gender(models.TextChoices):
    MALE = 'male', _('male')
    FEMALE = 'female', _('female')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)
    # gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class Roletype(models.TextChoices):
    ACTOR = 'actor', _('actor')
    WRITER = 'writer', _('writer')
    DIRECTOR = 'director', _('director')


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Roletype.choices, default=Roletype.ACTOR)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('Person film')
        verbose_name_plural = _('Persons films')
        index_together = [
            ["film_work_id", "person_id"],
            ["person_id", "film_work_id"],
        ]
