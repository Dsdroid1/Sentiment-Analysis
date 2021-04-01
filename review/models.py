from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    num_positive = models.IntegerField()
    num_negative = models.IntegerField()
    poster = models.FileField(upload_to='movies')
    def __str__(self):
        return self.title