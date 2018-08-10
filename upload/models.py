from django.db import models
from django.core.validators import validate_image_file_extension
from .helpers import RandomFileName

# Create your models here.


class ImageModel(models.Model):
    image_file = models.ImageField(upload_to=RandomFileName('raw_images'),
                                   blank=True,
                                   validators=[validate_image_file_extension])
    image_url = models.URLField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id



