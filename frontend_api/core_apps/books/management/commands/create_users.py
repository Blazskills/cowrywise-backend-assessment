from django.core.management.base import BaseCommand
from faker import Faker
from core_apps.books.models import BookUser
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Create 2000 fake users in the database'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users_to_create = []
        created_users_count = 0

        for _ in range(100000):  # Adjust the number of users to create here
            while True:
                try:
                    # Generate a unique email
                    email = fake.unique.email().lower().replace(" ", "")

                    # Check if the email already exists
                    if not BookUser.objects.filter(email=email).exists():
                        # If email is unique, create the user
                        user = BookUser(
                            email=email,
                            first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            user_type=fake.random_element(elements=("Admin", "Non-Admin"))
                        )
                        users_to_create.append(user)
                        created_users_count += 1
                        break  # Break out of the loop once a unique email is found and user is created
                except IntegrityError:
                    # If there's an IntegrityError (which shouldn't happen due to .exists()), retry
                    continue

            # Bulk insert users in batches of 1000 for performance optimization
            if len(users_to_create) >= 90000:
                BookUser.objects.bulk_create(users_to_create)
                users_to_create = []

        # Insert any remaining users not yet bulk created
        if users_to_create:
            BookUser.objects.bulk_create(users_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_users_count} users!'))
