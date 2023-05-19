import csv

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Review, Title, User


class Command(BaseCommand):
    help = 'Загрузка данных из csv файла в модель Review'

    def handle(self, *args, **options):
        with open('static/data/review.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    title = Title.objects.get(pk=row['title_id'])
                    author = User.objects.get(pk=row['author'])
                except ObjectDoesNotExist:
                    raise CommandError('Записи в базе данных не обнаружены!')
                new_review = Review(
                    id=row['id'],
                    title=title, text=row['text'],
                    author=author, score=row['score'],
                    pub_date=row['pub_date']
                )
                new_review.save()
        print('Импорт выполнен успешно!')
