from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Wipe demo data: delete all non-superuser users, which cascades to decks and flashcards."

    def handle(self, *args, **kwargs):
        # Delete all users that are NOT superusers
        users_deleted, _ = User.objects.filter(is_superuser=False).delete()
        self.stdout.write(f"Deleted {users_deleted} objects.")

        self.stdout.write(self.style.SUCCESS("Successfully wiped demo data."))