from django.db import models

class Timestamps(models.Model):
    """Abstract timestamp model
    :author:Muhammad Tareq
    :created:24-07-2018
    :last_edit:24-07-2018
    # """
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class SoftDelete(models.Model):
    """Abstract SoftDeletion model
        :author:Muhammad Tareq
    """
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
