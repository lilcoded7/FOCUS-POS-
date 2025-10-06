from django import forms
from shop.models.cancel_order import CancelOrder
from shop.models.products import Product, Category
from shop.models.workers import Worker



class CancelOrderForm(forms.Form):
    reason = forms.ModelChoiceField(
        queryset=CancelOrder.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Select a reason"}
        ),
    )
    context = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Optional notes about the cancellation",
            }
        ),
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "status",
            "image",
            "stock_quantity",
            "actual_price",
            "selling_price",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Product name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product description",
                    "rows": 3,
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "stock_quantity": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Quantity in stock"}
            ),
            "actual_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Cost price"}
            ),
            "selling_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Selling price"}
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class CreateWorkerForm(forms.ModelForm):
    
    class Meta:
        model = Worker
        fields = ["role", "name", "email", "phone_number", "id_card", "id_image"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class ActivationForm(forms.Form):
    code = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'id':'activation-code',
                'placeholder':'Enter activation code'

            }
        )
    )