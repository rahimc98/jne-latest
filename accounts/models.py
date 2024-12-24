from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy

from core.functions import generate_fields


class User(AbstractUser):
    usertype = models.CharField(
        max_length=128,
        choices=[
            ("Staff", "Staff"),
            ("Admin", "Admin"),
            ("Superadmin", "Superadmin")
        ],
        default="Staff",
    )
    password = models.CharField(max_length=128, null=True)

    def get_fields(self):
        return generate_fields(self)

    def get_absolute_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounts:user_list")

    def get_update_url(self):
        return reverse_lazy("accounts:user_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounts:user_delete", kwargs={"pk": self.pk})

    @property
    def fullname(self):
        return self.username

    def __str__(self):
        return self.username
