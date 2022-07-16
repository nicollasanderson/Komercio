from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(
        self,
        email,
        first_name,
        last_name,
        is_staff,
        is_superuser,
        password,
        is_seller=False,
        **extra_fields
    ):
        now = timezone.now()

        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_seller=is_seller,
            is_staff=is_staff,
            date_joined=now,
            username=email,
            is_superuser=is_superuser,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        return self._create_user(
            email, first_name, last_name, False, False, password, **extra_fields
        )

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(
            email, first_name, last_name, True, True, password, **extra_fields
        )
