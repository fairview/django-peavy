from django.db import models

class Quote(models.Model):
    text = models.TextField()
    show = models.CharField(max_length=256)
    character = models.CharField(max_length=256)
    submitter = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

