from django.core.management.base import BaseCommand
from faker import Faker
import random
from catalog.models import Author, Category, Book

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with Authors, Categories, and Books"

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int, default=20, help='Number of authors to create')
        parser.add_argument('--categories', type=int, default=10, help='Number of categories to create')
        parser.add_argument('--books', type=int, default=100, help='Number of books to create')
        parser.add_argument('--flush', action='store_true', help='Delete old data before seeding')

    def handle(self, *args, **kwargs):
        authors_count = kwargs['authors']
        categories_count = kwargs['categories']
        books_count = kwargs['books']
        flush = kwargs['flush']

        if flush:
            self.stdout.write(self.style.WARNING("Flush skipped: Keeping previous data."))


        # Create Authors
        authors = [
            Author.objects.create(
                name=fake.name(),
                biography=fake.paragraph(nb_sentences=5)
            ) for _ in range(authors_count)
        ]
        self.stdout.write(self.style.SUCCESS(f"Created {authors_count} authors"))

        # Create Categories
        categories = [
            Category.objects.create(
                name=fake.unique.word().capitalize(),
                description=fake.sentence()
            ) for _ in range(categories_count)
        ]
        self.stdout.write(self.style.SUCCESS(f"Created {categories_count} categories"))

        # Create Books
        for _ in range(books_count):
            Book.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=200),
                price=round(random.uniform(5, 100), 2),
                stock=random.randint(0, 50),
                author=random.choice(authors),
                category=random.choice(categories),
                pub_date=fake.date_between(start_date='-5y', end_date='today')
            )
        self.stdout.write(self.style.SUCCESS(f"Created {books_count} books"))
