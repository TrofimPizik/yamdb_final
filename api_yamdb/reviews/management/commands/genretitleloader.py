import csv
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from reviews.models import Title, Genre, GenreTitle


class Command(BaseCommand):
    help = 'Загрузка данных из csv файла в модель GenreTitle'

    def handle(self, *args, **options):
        with open('static/data/genre_title.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    genre = Genre.objects.get(pk=row['genre_id'])
                    title = Title.objects.get(pk=row['title_id'])
                except ObjectDoesNotExist:
                    raise CommandError('Записи в базе данных не обнаружены!')
                new_genre_title = GenreTitle(
                    id=row['id'], title=title,
                    genre=genre
                )
                new_genre_title.save()
        print('Импорт выполнен успешно!')
