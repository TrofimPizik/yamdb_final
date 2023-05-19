import csv
from django.core.management.base import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    help = 'Загрузка данных из csv файла в модель Category'

    def handle(self, *args, **options):
        with open('static/data/category.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_category = Category(
                    id=row['id'], name=row['name'],
                    slug=row['slug']
                )
                new_category.save()
        print('Импорт выполнен успешно!')
