from django.db import models

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(max_length=100, default="General")


    views = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.text[:50]
