import csv

from django.core.management.base import BaseCommand
from reviews.models import Genre


class Command(BaseCommand):
    help = 'Загрузка данных из csv файла в модель Genre'

    def handle(self, *args, **options):
        with open('static/data/genre.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_genre = Genre(
                    id=row['id'], name=row['name'],
                    slug=row['slug']
                )
                new_genre.save()
        print('Импорт выполнен успешно!')
