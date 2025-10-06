from django.db import models
from setup.basemodel import BaseModel
from shop.models.orders import Order
from shop.models.products import Product
from decimal import Decimal

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}"

    def get_total_product_price(self):
        if self.product and self.product.selling_price:
            return self.quantity * self.product.selling_price
        return Decimal('0.00')