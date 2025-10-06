from setup.basemodel import BaseModel
from django.db import models


class Rider(BaseModel):
    name = models.CharField(max_length=100)
    phne_number = models.CharField(max_length=100)
    id_card = models.CharField(max_length=100, null=True, blank=True)
    id_image = models.ImageField(null=True, blank=True)
    

    def __str__(self):
        return self.name 
    