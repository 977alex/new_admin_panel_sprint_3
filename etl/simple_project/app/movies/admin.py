from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
    search_fields = ('name', 'description')
    list_filter = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    raw_id_fields = ('film_work', 'genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    raw_id_fields = ('film_work', 'person',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        # 'get_genres',
    )
    raw_id_fields = ('genres',)
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )

    # list_prefetch_related = ('genres',)
    # def get_queryset(self, request):
    #     queryset = (
    #         super().get_queryset(request)
    #         .prefetch_related(*self.list_prefetch_related)
    #     )
    #     return queryset
    #
    # def get_genres(self, obj):
    #     return ','.join([genre.name for genre in obj.genres.all()])
    #
    # get_genres.short_description = 'Жанры фильма'

    # Фильтрация в списке
    list_filter = (
        'type',
        'rating',
    )
    # Поиск по полям
    search_fields = ('title', 'description',)
