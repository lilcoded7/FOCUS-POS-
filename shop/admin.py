from django.contrib import admin
from shop.models.orders import Order
from shop.models.order_items import OrderItem
from shop.models.products import Product, Category
from shop.models.workers import Worker
from shop.models.reports import Report
from shop.models.cancel_order import CancelOrder
from shop.models.activate_accounts import ActivateAccount, POS
from shop.models.customers import Customer
from shop.models.riders import Rider
from django.core.exceptions import ValidationError
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'total_price']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'status']


admin.site.register(ActivateAccount)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Worker)
admin.site.register(Report)
admin.site.register(CancelOrder)
admin.site.register(Customer)
admin.site.register(Rider)

@admin.register(POS)
class POSAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
       
        return not POS.objects.exists()

    def has_delete_permission(self, request, obj=None):
      
        return False

    def get_queryset(self, request):
        
        POS.objects.get_or_create(pk=1)
        return super().get_queryset(request)