from django.urls import path
from shop.views import *


urlpatterns = [
    path("", home, name="home"),
    path("add-to-order/<int:product_id>/", add_to_order, name="add_to_order"),
    path(
        "update-order-item/<int:item_id>/", update_order_item, name="update_order_item"
    ),
    path('search-customers/', search_customers, name='search_customers'),
    path("complete-order/", complete_order, name="complete_order"),
    path("get-active-order/", get_active_order, name="get_active_order"),
    path("get-recent-orders/", get_recent_orders, name="get_recent_orders"),
    path("cancel-order/<int:order_id>/", cancel_order, name="cancel_order"),
    path("products/<int:product_id>/detail/", product_detail, name="product_detail"),
    path("products/<int:product_id>/delete/", delete_product, name="delete_product"),
    path("products/", products, name="products"),
    path("reports/", reports, name="reports"),
    path("orders/", orders, name="orders"),
    path("orders/filter/", filter_orders, name="filter_orders"),
    path("orders/<int:order_id>/delete/", delete_order, name="delete_order"),
    path("reports/filter/", filter_reports, name="filter_reports"),
    path("reports/<int:report_id>/detail/", report_detail, name="report_detail"),
    path("reports/<int:report_id>/delete/", delete_report, name="delete_report"),
    path(
        "get-order-details/<int:order_id>/", get_order_details, name="get_order_details"
    ),
    path("create/product/", product_inventory, name="product_inventory"),
    path("<int:product_id>/detail/", product_detail, name="product_detail"),
    path("<int:product_id>/delete/", delete_product, name="delete_product"),
    path("workers/", workers, name="workers"),
    path("delete_worker/<int:worker_id>", delete_worker, name="delete_worker"),
    path("create_worker/", create_worker, name="create_worker"),
    path(
        "api/get/activated/code",
        ActivationAPIView.as_view(),
        name="get_activating_code",
    ),
    path("activate/account/", activate_account, name="activate_account"),
    path("order/details/<int:order_id>", view_order, name="view_order_details"),
    path('order/invoice/<int:order_id>', order_invoice, name='order_invoice'),

    path('order/<int:order_id>/assign-rider/', assign_order_rider, name='assign_order_rider'),
    path('create-rider/', create_rider, name='create_rider'),
    path('order/<int:order_id>/remove-rider/', remove_rider_from_order, name='remove_rider_from_order'),
]
