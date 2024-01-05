from django.db import models
from django.db.models import CharField

from .utils import secret_id, phone_validation


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserInfoDetails(BaseModel):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, unique=True, validators=[phone_validation()])
    email = models.EmailField(unique=False)

    def __str__(self) -> CharField:
        return self.name


class Transaction(BaseModel):
    transaction_name = models.CharField(max_length=155, blank=False, null=False, verbose_name="name", default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(verbose_name="Transaction date")
    user_info = models.ForeignKey(
        UserInfoDetails,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_info",
    )
    transaction_id = models.CharField(max_length=255, default=secret_id(4), unique=True)

    def __str__(self) -> str:
        return f"{self.user_info.name}  -  {self.transaction_date.date()}"
