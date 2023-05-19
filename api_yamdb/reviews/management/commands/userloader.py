import csv
from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Загрузка данных из csv файла в модель User'

    def handle(self, *args, **options):
        with open('static/data/users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_user = User(
                    id=row['id'],
                    username=row['username'], email=row['email'],
                    role=row['role'], bio=row['bio'],
                    first_name=row['first_name'], last_name=row['last_name']
                )
                new_user.save()
        print('Импорт выполнен успешно!')
