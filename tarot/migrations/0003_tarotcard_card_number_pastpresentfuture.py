# Generated by Django 4.1 on 2022-08-23 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarot', '0002_alter_tarotcard_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarotcard',
            name='card_number',
            field=models.IntegerField(default=0, max_length=2),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='pastPresentFuture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=1000)),
                ('past_reversed', models.BooleanField(default=False)),
                ('present_reversed', models.BooleanField(default=False)),
                ('future_reversed', models.BooleanField(default=False)),
                ('cards', models.ManyToManyField(related_name='pk', to='tarot.tarotcard')),
            ],
        ),
    ]
