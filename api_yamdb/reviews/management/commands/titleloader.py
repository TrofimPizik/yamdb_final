import csv
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from reviews.models import Title, Category


class Command(BaseCommand):
    help = 'Загрузка данных из csv файла в модель Title'

    def handle(self, *args, **options):
        with open('static/data/titles.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    category = Category.objects.get(pk=row['category'])
                except ObjectDoesNotExist:
                    raise CommandError('Записи в базе данных не найдены!')
                new_title = Title(
                    id=row['id'], name=row['name'],
                    year=row['year'], category=category)
                new_title.save()
        print('Импорт выполнен успешно!')
