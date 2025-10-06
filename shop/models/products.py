from setup.basemodel import BaseModel
from django.db import models


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    STATUS = [
        ('active', 'Active (In Stock)'),
        ('inactive', 'Out of Stock'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS)
    image = models.ImageField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)

    actual_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Name: {self.name} Price: {self.selling_price}"