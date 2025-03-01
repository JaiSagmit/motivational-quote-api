from django.db import models

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    mood = models.CharField(max_length=100, blank=True, null=True)
    length = models.IntegerField()
    is_popular = models.BooleanField(default=False)
    # Add other fields like 'theme', 'celebrity', etc., as per your requirements.

    def __str__(self):
        return self.text
from django.db import models

