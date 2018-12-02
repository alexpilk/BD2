from django.db import models


class RodzajeSprzetu(models.Model):
    # song title
    nazwa = models.CharField(max_length=255)

    def __str__(self):
        return self.nazwa
