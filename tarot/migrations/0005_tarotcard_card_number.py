# Generated by Django 4.1 on 2022-08-23 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarot', '0004_remove_tarotcard_card_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarotcard',
            name='card_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]