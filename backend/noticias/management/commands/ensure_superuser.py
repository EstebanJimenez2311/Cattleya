import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea o actualiza un superusuario usando variables DJANGO_SUPERUSER_*."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "").strip()

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Saltando ensure_superuser: faltan variables DJANGO_SUPERUSER_USERNAME, "
                    "DJANGO_SUPERUSER_EMAIL o DJANGO_SUPERUSER_PASSWORD."
                )
            )
            return

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superusuario creado: {username}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superusuario actualizado: {username}"))
