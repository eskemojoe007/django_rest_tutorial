from django.db import models

# Create your models here.
class Poll(model.Models):
    question = models.CharField(max_length=100)
