# Generated by Django 3.2 on 2023-05-13 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230513_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=4, verbose_name='код подтверждения'),
        ),
    ]
