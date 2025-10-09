from django.db import models
from setup.basemodel import BaseModel
from shop.models.customers import Customer
from shop.models.riders import Rider
from django.db.models import Max
from decimal import Decimal

class Order(BaseModel):
    status_choices = [
        ("pending", "pending"),
        ("success", "success"),
        ("wish_list", "Wish List"),
    ]
    printing_choices = [
        ("printed", "printed"),
        ("pending", "pending"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    rider = models.ForeignKey(Rider, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default="pending")
    order_printed = models.CharField(default=printing_choices, max_length=100, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by "

    def save(self, *args, **kwargs):
        if not self.order_id:
            max_id = Order.objects.aggregate(Max("id"))["id__max"] or 0
            self.order_id = f"#ORD-{max_id + 1}"
        super().save(*args, **kwargs)

    def get_total_price(self):
        total_order_price = sum(
            (item.get_total_product_price() for item in self.items.all()),
            Decimal('0.00')  
        )
        return total_order_price

    def get_order_quantity(self):
        order_quantity = self.items.count()
        return order_quantity if order_quantity else 0.00


