from django.db import models

# Create your models here.


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
