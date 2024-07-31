# your_app/management/commands/populate_books.py
from django.core.management.base import BaseCommand
from faker import Faker
from your_app.models import Book
import requests
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Populates the database with dummy Book data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(10):  # Generate 10 fake books
            book = Book(
                name=fake.sentence(nb_words=3),
                isbn=fake.isbn10(),
                category=fake.random_element(elements=('Fiction', 'Non-fiction', 'Sci-fi', 'Fantasy')),
                author=fake.name(),
                publication=fake.company(),
                description=fake.paragraph(),
                quantity=fake.random_int(min=1, max=50),
                availability=fake.boolean(chance_of_getting_true=80),  # 80% chance of being available
            )

            # Generate and save a dummy image
            image_url = fake.image_url(width=800, height=600)  # Generate a random image URL
            image_name = os.path.basename(image_url)
            response = requests.get(image_url)
            if response.status_code == 200:
                book.image.save(image_name, File(response.raw))

            book.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy Book data.'))
