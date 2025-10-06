from datetime import datetime, time
import calendar
import time as time_module  # Renamed to avoid conflict
import requests
from django.core.exceptions import ValidationError
from django.utils import timezone
from shop.models.activate_accounts import POS

def check_and_turn_off_live_two():
    """Check if it's the 28th of the month and turn off live mode"""
    current_time = time_module.localtime()  # Use time_module instead of time
    day = current_time.tm_mday
    
    if day == 28:
        pos_config = POS.load()
        pos_config.is_live = False
        pos_config.save()
    return day

def check_and_turn_off_live():
    """Check if it's the 28th of the month and turn off live mode"""
    current_time = time_module.localtime()  # Use time_module instead of time
    day = current_time.tm_mday
    
    if day == 28:
        pos_config = POS.load()
        pos_config.is_live = False
        pos_config.save()
    return day

def verify_code(request, code: str):
    """Verify activation code with the API"""
    url = f"https://focuspos.pythonanywhere.com/api/get/activated/code"

    try:
        response = requests.post(url, data={"code": code})
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success":
            pos_config = POS.load()
            if len(code) == 6:
                pos_config.always_live = True
                pos_config.is_live=True
            elif len(code) == 4:
                pos_config.is_live = True
            else:
                raise ValidationError("Invalid code length")
            pos_config.save()
            return {"status": "success", "message": data.get("message", "Code verified")}
        return {"status": "failed", "error": data.get("message", "Verification failed")}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error": f"{e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def has_activated_account(request):
    """Check if account is activated and logout if not"""
    pos_config = POS.load()
    if not pos_config.is_live and not pos_config.always_live:
        from django.contrib import messages
        from django.contrib.auth import logout
        from django.shortcuts import redirect
        
        messages.error(request, "Contact Support to activate your account.")
        logout(request)
        return redirect("login_view")
    return None

def get_order_items_data(order):
    """Get order items data for JSON response"""
    return [
        {
            "id": item.id,
            "product_id": item.product.id if item.product else None,
            "product_name": item.product.name if item.product else "Product not available",
            "product_price": float(item.product.selling_price) if item.product else 0.0,
            "quantity": item.quantity,
        }
        for item in order.items.all()
    ]

def get_date_range(time_filter, custom_date=None):
    """Get start and end datetime based on time filter"""
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    if time_filter == "today":
        return today_start, today_end
    elif time_filter == "yesterday":
        return today_start - timedelta(days=1), today_start
    elif time_filter == "week":
        return today_start - timedelta(days=today_start.weekday()), today_end
    elif time_filter == "month":
        return today_start.replace(day=1), today_end
    elif time_filter == "custom" and custom_date:
        try:
            custom_date = datetime.strptime(custom_date, "%Y-%m-%d")
            start_date = timezone.make_aware(custom_date)
            return start_date, start_date + timedelta(days=1)
        except ValueError:
            raise ValueError("Invalid date format")
    else:
        raise ValueError("Invalid time filter")

def format_order_data(order):
    """Format order data for JSON response"""
    return {
        "id": order.id,
        "order_id": order.order_id,
        "created_at": order.created_at.strftime("%Y-%m-%d %H:%M"),
        "item_count": order.get_order_quantity(),
        "total_price": float(order.total_price),
        "status": order.status,
        "status_display": order.get_status_display(),
    }

def format_report_data(report):
    """Format report data for JSON response"""
    return {
        "id": report.id,
        "created_at": report.created_at.strftime("%Y-%m-%d %H:%M"),
        "context": report.context,
        "dec": report.dec,
        "order_id": report.order.id if report.order else None,
        "order_number": report.order.order_id if report.order else None,
    }

def create_report(user, context, dec, order=None):
    """Helper function to create reports"""
    from shop.models.reports import Report
    Report.objects.create(
        user=user,
        order=order,
        context=context,
        dec=dec,
    )