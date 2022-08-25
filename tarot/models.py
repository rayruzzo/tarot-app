from django.db import models

# Create your models here.
class tarotCard(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="tarot/cards")
    meaning = models.TextField(max_length=2000)
    reversed_meaning = models.TextField(max_length=2000)

    def __str__(self):
        return self.name

