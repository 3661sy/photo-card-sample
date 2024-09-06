from django.contrib.auth.models import User
from django.db import models


class PhotoCard(models.Model):
    name = models.CharField(max_length=200)
    group_name = models.CharField(max_length=100)
    member_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = '포토카드'
        verbose_name_plural = verbose_name


class Sale(models.Model):
    photo_card = models.ForeignKey(PhotoCard, on_delete=models.CASCADE, related_name='photo_card')

    price = models.PositiveIntegerField(default=0, help_text='가격')
    fee = models.PositiveIntegerField(default=0, help_text='수수료')

    SALE_STATE = (
        ('ING', '판매중'),
        ('END', '판매중')
    )
    state = models.CharField(max_length=8, choices=SALE_STATE, default='ING')

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')

    create_date = models.DateTimeField(auto_now_add=True)
    renewal_date = models.DateTimeField(auto_now=True)
    sold_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name = '판매 목록'
        verbose_name_plural = verbose_name
