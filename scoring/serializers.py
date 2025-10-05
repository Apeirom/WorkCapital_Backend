# scoring/serializers.py
from rest_framework import serializers
from .models import Financing

class FinancingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financing
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'amount_invested')