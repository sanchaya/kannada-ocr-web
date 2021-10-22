from django.db import models

# Create your models here.
class FileStatus(models.Model):
    file = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.file