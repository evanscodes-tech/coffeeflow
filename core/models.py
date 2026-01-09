from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Farmer(models.Model):
    farmer_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=200, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.farmer_id})"

class Delivery(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='deliveries')
    cherry_kg = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    kg_dry = models.DecimalField(max_digits=6, decimal_places=2, editable=False)
    price_per_kg = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('120.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    delivery_time = models.DateTimeField(auto_now_add=True)
    recorded_by = models.CharField(max_length=100, blank=True)
    
    # SMS tracking fields
    sms_sent = models.BooleanField(default=False)
    sms_status = models.CharField(max_length=50, blank=True)
    
    def save(self, *args, **kwargs):
        # Calculate kgs and total
        conversion_factor = Decimal('0.20')
        self.kg_dry = round(self.cherry_kg * conversion_factor, 2)
        self.total_amount = self.kg_dry * self.price_per_kg
        
        # Save first (to get ID if new)
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Send SMS after save (only for new deliveries)
        if is_new:
            from .sms import send_delivery_confirmation
            try:
                send_delivery_confirmation(self)
            except Exception as e:
                print(f"Failed to send SMS: {e}")
    
    def __str__(self):
        return f"{self.farmer.name} - {self.cherry_kg}kg cherry on {self.delivery_time.date()}"

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='payments')
    period_start = models.DateField()
    period_end = models.DateField()
    total_kg_dry = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Payment to {self.farmer.name} for {self.period_start} to {self.period_end}"