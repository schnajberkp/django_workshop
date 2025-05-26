from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector = models.BooleanField(default=False)
    booked = models.BooleanField(default=False)

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('room', 'date')

    def __str__(self):
        return self.name