from django.db import models
from django.conf import settings


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subfolders'
    )
    is_root = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_folders')

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

    def share_files(self, user):
        for file in self.files.all():
            file.shared_with.add(user)

    def share_subfolders(self, user):
        for folder in self.subfolders.all():
            folder.shared_with.add(user)
            folder.share_files(user)
            folder.share_subfolders(user)


class File(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("Folder", on_delete=models.CASCADE, related_name='files')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_files')

    def __str__(self):
        return self.name
