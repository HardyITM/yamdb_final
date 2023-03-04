import csv
import os

from django.core.management.base import BaseCommand
from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)

APP_PATH = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)
DATA_PATH = os.path.join(APP_PATH, "static/data/")


class Command(BaseCommand):
    help = "Наполнение базы данных данными из csv файлов."

    def handle(self, *args, **options):
        self.stdout.write("Начат импорт данных...")

        for filename, model in MODEL_FILENAME_MAPPING.items():
            filepath = os.path.join(DATA_PATH, filename)

            with open(filepath, mode="r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file, delimiter=",")
                self.stdout.write(f"Создание объектов модели {model.__name__}")

                for row in reader:
                    if "category" in row:
                        category = Category.objects.get(id=row["category"])
                        row["category"] = category

                    if "genre" in row:
                        genre = Genre.objects.get(id=row["genre"])
                        row["genre"] = genre

                    if "author" in row:
                        author = User.objects.get(id=row["author"])
                        row["author"] = author

                    model.objects.get_or_create(**row)

        self.stdout.write("Импорт данных завершён.")


MODEL_FILENAME_MAPPING = {
    "users.csv": User,
    "category.csv": Category,
    "genre.csv": Genre,
    "titles.csv": Title,
    "genre_title.csv": GenreTitle,
    "review.csv": Review,
    "comments.csv": Comment,
}
