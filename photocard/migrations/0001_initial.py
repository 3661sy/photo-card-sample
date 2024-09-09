# Generated by Django 4.2.16 on 2024-09-09 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('group_name', models.CharField(max_length=100)),
                ('member_name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': '포토카드',
                'verbose_name_plural': '포토카드',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(default=0, help_text='가격')),
                ('fee', models.PositiveIntegerField(default=0, help_text='수수료')),
                ('state', models.CharField(choices=[('ING', '판매중'), ('END', '판매완료')], default='ING', max_length=8)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('renewal_date', models.DateTimeField(auto_now=True)),
                ('sold_date', models.DateTimeField(null=True)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('photo_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_card', to='photocard.photocard')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '판매 목록',
                'verbose_name_plural': '판매 목록',
            },
        ),
    ]
