from rest_framework import serializers
from shop.models.activate_accounts import ActivateAccount, POS


class ActivateAccountSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = ActivateAccount
        fields = ["code"]

    def validate(self, attrs):
        code = attrs.get("code")

        if not ActivateAccount.objects.filter(code=code, is_expired=False).exists():
            raise serializers.ValidationError("Invalid Activation Code")

        if not code.isdigit():
            raise serializers.ValidationError("Code must be numeric")

        return attrs