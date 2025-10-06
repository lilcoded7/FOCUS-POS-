from setup.basemodel import BaseModel
from django.db import models


class Customer(BaseModel):
    name = models.CharField(max_length=100, default='customer')
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return str(self.phone_number)