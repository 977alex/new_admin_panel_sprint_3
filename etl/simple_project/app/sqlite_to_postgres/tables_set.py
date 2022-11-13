from models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


def get_tables_set() -> dict:

    tables_set = {}

    tables_set['genre'] = {
        'dataclass': Genre,
        'fields': ['id', 'name', 'description'],
        'service_fields': ['created', 'modified'],
    }

    tables_set['person'] = {
        'dataclass': Person,
        'fields': ['id', 'full_name'],
        'service_fields': ['created', 'modified'],
    }

    tables_set['film_work'] = {
        'dataclass': Filmwork,
        'fields': ['id', 'title', 'description', 'creation_date', 'rating', 'type', ],
        'service_fields': ['created', 'modified'],
    }

    tables_set['genre_film_work'] = {
        'dataclass': GenreFilmwork,
        'fields': ['id', 'genre_id', 'film_work_id'],
        'service_fields': ['created'],
    }

    tables_set['person_film_work'] = {
        'dataclass': PersonFilmwork,
        'fields': ['id', 'person_id', 'film_work_id', 'role'],
        'service_fields': ['created'],
    }

    return tables_set
