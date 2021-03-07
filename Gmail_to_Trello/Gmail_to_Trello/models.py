from django.db import models


class Mail(models.Model):
    snippet = models.CharField(max_length=200)

    def __str__(self):
        return self.snippet
