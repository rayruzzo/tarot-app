# Generated by Django 4.1 on 2022-08-23 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarotcard',
            name='image',
            field=models.ImageField(upload_to='tarot/cards'),
        ),
    ]