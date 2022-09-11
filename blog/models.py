from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    content = models.CharField(max_length=10000, null=False, blank=False)
    image_url = models.URLField(max_length=1024, blank=True)

    def __str__(self):
        return self.title
