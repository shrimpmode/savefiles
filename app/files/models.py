from django.db import models
from django.conf import settings


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_root = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'is_root'],
                condition=models.Q(is_root=True),
                name='unique_root_folder_per_user'
            ),
            models.CheckConstraint(
                check=~models.Q(is_root=True, parent__isnull=False),
                name='root_folder_cannot_have_parent'
            ),
        ]

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("Folder", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
