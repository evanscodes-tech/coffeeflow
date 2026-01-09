from django.contrib import admin
from django.utils.html import format_html
from .models import Farmer, Delivery, Payment

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('farmer_id', 'name', 'phone', 'location', 'date_registered', 'total_deliveries', 'total_kg_dry')
    search_fields = ('farmer_id', 'name', 'phone')
    list_filter = ('location', 'date_registered')
    readonly_fields = ('date_registered',)
    
    def total_deliveries(self, obj):
        return obj.deliveries.count()
    total_deliveries.short_description = 'Total Deliveries'
    
    def total_kg_dry(self, obj):
        from django.db.models import Sum
        result = obj.deliveries.aggregate(Sum('kg_dry'))
        return result['kg_dry__sum'] or 0
    total_kg_dry.short_description = 'Total Dry Weight (kg)'

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'farmer_info', 'cherry_kg', 'kg_dry', 'total_amount', 'delivery_time', 'sms_status_badge', 'recorded_by')
    list_filter = ('delivery_time', 'sms_sent', 'recorded_by')
    search_fields = ('farmer__name', 'farmer__farmer_id', 'recorded_by')
    readonly_fields = ('kg_dry', 'total_amount', 'delivery_time', 'sms_sent', 'sms_status')
    date_hierarchy = 'delivery_time'
    actions = ['resend_sms_simulation', 'mark_sms_as_failed']
    
    def farmer_info(self, obj):
        return f"{obj.farmer.name} ({obj.farmer.farmer_id})"
    farmer_info.short_description = 'Farmer'
    
    def sms_status_badge(self, obj):
        if obj.sms_sent and obj.sms_status:
            color = 'green' if obj.sms_status == 'success' else 'orange'
            status_text = obj.sms_status
        elif obj.sms_sent:
            color = 'gray'
            status_text = 'Sent'
        else:
            color = 'gray'
            status_text = 'Not Sent'
        
        return format_html(
            '<span style="color: white; background: {}; padding: 3px 8px; border-radius: 10px;">{}</span>',
            color, status_text
        )
    sms_status_badge.short_description = 'SMS Status'
    
    def resend_sms_simulation(self, request, queryset):
        from .sms import send_delivery_confirmation
        count = 0
        for delivery in queryset:
            if not delivery.sms_sent:
                send_delivery_confirmation(delivery)
                count += 1
        self.message_user(request, f"Resent SMS for {count} deliveries.")
    resend_sms_simulation.short_description = "Resend SMS (simulation)"
    
    def mark_sms_as_failed(self, request, queryset):
        updated = queryset.update(sms_status='failed')
        self.message_user(request, f"Marked SMS status as 'failed' for {updated} deliveries.")
    mark_sms_as_failed.short_description = "Mark SMS as failed"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'farmer_info', 'period_start', 'period_end', 'total_kg_dry', 'total_amount', 'status_badge', 'payment_date')
    list_filter = ('status', 'period_start', 'period_end')
    search_fields = ('farmer__name', 'farmer__farmer_id')
    readonly_fields = ('total_kg_dry', 'total_amount')
    
    def farmer_info(self, obj):
        return f"{obj.farmer.name} ({obj.farmer.farmer_id})"
    farmer_info.short_description = 'Farmer'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: white; background: {}; padding: 3px 8px; border-radius: 10px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'