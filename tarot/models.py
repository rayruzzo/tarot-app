from django.db import models

# Create your models here.
class reading(models.Model):
    user = models.CharField(max_length=100)
    question = models.CharField(max_length=500)
    cards = models.CharField(max_length=500)

    def __str__(self):
        return self.user + " - " + self.question + " - " + self.cards