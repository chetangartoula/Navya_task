from rest_framework import serializers

from transaction_api.models import UserInfoDetails, Transaction
from transaction_api.utils import secret_id, phone_validation

from django.db.models import Q


class UserInfoDetailsSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=15, validators=[phone_validation()])
    email = serializers.EmailField()

    class Meta:
        model = UserInfoDetails
        fields = ["name", "phone", "email"]


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        allow_null=False, decimal_places=2, max_digits=100
    )
    transaction_date = serializers.DateTimeField(allow_null=False)
    transaction_id = serializers.CharField(read_only=True)
    email = serializers.EmailField(source='user_info.email',allow_blank=False,allow_null=False)
    phone = serializers.CharField(allow_null=False, source="user_info.phone",validators=[phone_validation()])
    name = serializers.CharField(max_length=155, allow_blank=False, allow_null=False)

    class Meta:
        model = Transaction
        fields = ["id", "transaction_date", "amount", "name", "transaction_id", "email", "phone"]

    def create(self, validated_data):
        user_data = validated_data.pop("user_info", None)
        email = user_data.get("email", None)
        phone = user_data.get("phone", None)
        name = validated_data.pop("name",None)
        user_info = UserInfoDetails.objects.filter(Q(email=email) and Q(phone=phone)).first()
        if user_info:
            raise serializers.ValidationError({"error":"Email or Phone is already registered try with different email "
                                                       "or phone"},400)
        user_info = UserInfoDetails.objects.create(**user_data,name=name)
        transaction_id = secret_id(4)
        transaction = Transaction.objects.create(
            **validated_data, user_info=user_info, transaction_id=transaction_id,transaction_name=name
        )

        return transaction

    def update(self, instance, validated_data):
        user_info_data = validated_data.pop("user_info", None)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.transaction_date = validated_data.get(
            "transaction_date", instance.transaction_date
        )
        instance.transaction_name = validated_data.get("name",instance.transaction_name)
        if user_info_data:
            user_info = instance.user_info
            user_info.__dict__.update(user_info_data)
            instance.user_info = user_info
        instance.save()
        return instance
    

    def to_representation(self, instance):
        instance.name = instance.transaction_name
        data =super().to_representation(instance)
        data["transaction_date"] = instance.transaction_date.date()
        return data

