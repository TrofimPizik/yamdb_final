import csv

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Comment, Review, User


class Command(BaseCommand):
    help = 'Загрузка данных из csv файла в модель Comment'

    def handle(self, *args, **options):
        with open('static/data/comments.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    review = Review.objects.get(pk=row['review_id'])
                    author = User.objects.get(pk=row['author'])
                except ObjectDoesNotExist:
                    raise CommandError('Записи в базе данных не обнаружены!')
                new_comment = Comment(
                    id=row['id'],
                    review=review, text=row['text'],
                    author=author, pub_date=row['pub_date']
                )
                new_comment.save()
        print('Импорт выполнен успешно!')
