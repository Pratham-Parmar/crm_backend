from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Port(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


# class Exim(models.Model):
#     exim = (
#         ('Import', 'Import'),
#         ('Export', 'Export'),
#     )


class Rates(models.Model):
    container_sizes = (
        ('20', '20'),
        ('40', '40'),
        ('40hq', '40hq'),
    )
    source = models.ForeignKey(Port, on_delete=models.PROTECT, related_name='source')
    destination = models.ForeignKey(Port, on_delete=models.PROTECT, related_name='destination')
    container_size = models.CharField(max_length=5, choices=container_sizes)
    name = models.CharField(max_length=10)
    rate = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
