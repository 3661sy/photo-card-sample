from django.contrib.auth.models import User
from django.db import models


class Cash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '충전금'
        verbose_name_plural = verbose_name

