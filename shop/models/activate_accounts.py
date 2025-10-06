from django.db import models
from setup.basemodel import BaseModel
from django.core.exceptions import ValidationError

class ActivateAccount(BaseModel):
    code = models.CharField(max_length=100)
    is_expired = models.BooleanField(default=False)


class POS(BaseModel):
    is_live = models.BooleanField(default=False)
    always_live = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and POS.objects.exists():
            raise ValidationError('Only one POS configuration instance can be created')
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def delete(self, *args, **kwargs):
        raise ValidationError('Cannot delete the POS configuration instance')

    class Meta:
        verbose_name = 'POS Configuration'
        verbose_name_plural = 'POS Configuration'
