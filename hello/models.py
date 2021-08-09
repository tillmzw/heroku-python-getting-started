import random

from django.db import models


# Create your models here.
class Greeting(models.Model):

    class EXCLAMATION(models.TextChoices):
        GERMAN = "Hallo"
        ENGLISH = "Hello"
        ROMONTSCH = "Tgau"
        ITALIAN = "Ciao"

    when = models.DateTimeField("date created", auto_now_add=True)
    exclamation = models.CharField(max_length=32, choices=EXCLAMATION.choices, default=EXCLAMATION.ENGLISH)

    @classmethod
    def random(cls):
        greeting = cls()
        greeting.exclamation = random.choice(cls.EXCLAMATION.values)
        greeting.save()
        return greeting

    def serialize(self):
        return {
            'when': self.when.isoformat(),
            'exclamation': self.exclamation,
            'exclamation_lang': Greeting.EXCLAMATION(self.exclamation).name
        }
