from rest_framework import serializers
from .models import Farmer, Delivery, Payment

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.name', read_only=True)
    farmer_phone = serializers.CharField(source='farmer.phone', read_only=True)
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'farmer', 'farmer_name', 'farmer_phone',
            'cherry_kg', 'kg_dry', 'price_per_kg', 'total_amount',
            'delivery_time', 'recorded_by', 'sms_sent', 'sms_status'
        ]
        read_only_fields = ('kg_dry', 'total_amount', 'delivery_time', 'sms_sent', 'sms_status')

class PaymentSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'