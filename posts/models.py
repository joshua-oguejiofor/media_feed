from django.conf import settings
from django.db import models



class Post(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'
    FILE = 'file'
    MEDIA_TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (FILE, 'file'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=280, blank=True)
    media_file = models.FileField(upload_to='posts/', max_length=1000)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} - {self.media_type} - {self.created_at:%Y-%m-%d}'

    