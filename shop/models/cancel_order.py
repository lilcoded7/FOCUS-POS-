from django.db import models
from setup.basemodel import BaseModel

class CancelOrder(BaseModel):
    reason = models.CharField(max_length=100)
    

    def __str__(self):
        return self.reason