import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def send_sms_simulation(phone_number, message):
    """Simulate SMS sending - logs instead of actually sending."""
    # In real system: integrate with Africa's Talking/Twilio here
    logger.info(f"[SIMULATED SMS] To: {phone_number}")
    logger.info(f"[SIMULATED SMS] Message: {message}")
    
    # Format for better console display
    print("\n" + "="*50)
    print("📱 COFFEE DELIVERY SMS NOTIFICATION")
    print("="*50)
    print(f"To: {phone_number}")
    print("-"*50)
    print(f"{message}")
    print("="*50)
    print("💡 In production, this would send via Africa's Talking API")
    print("="*50 + "\n")
    
    return {"status": "success", "message_id": "simulated_coffee_123"}

def send_delivery_confirmation(delivery):
    """Send confirmation SMS to farmer after coffee cherry delivery."""
    farmer = delivery.farmer
    
    # Coffee-specific message with conversion details
    message = (
        f"Habari {farmer.name}. "
        f"Mzigo wako wa kahawa: {delivery.cherry_kg}kg za buni "
        f"({delivery.kg_dry}kg kavu) umeandikwa. "
        f"Kiasi: KES {delivery.total_amount}. "
        f"Asante kwa kutoa kahawa bora!"
    )
    
    # Alternative in English:
    # message = (
    #     f"Hello {farmer.name}, "
    #     f"your coffee cherry delivery of {delivery.cherry_kg}kg "
    #     f"({delivery.kg_dry}kg dry) has been recorded. "
    #     f"Amount: KES {delivery.total_amount}. "
    #     f"Thank you for delivering quality coffee!"
    # )
    
    result = send_sms_simulation(farmer.phone, message)
    
    # Update delivery with SMS status
    delivery.sms_sent = True
    delivery.sms_status = result["status"]
    delivery.save(update_fields=['sms_sent', 'sms_status'])
    
    return result

def send_payment_notification(payment):
    """Send SMS when payment is processed to farmer."""
    farmer = payment.farmer
    
    message = (
        f"Habari {farmer.name}. "
        f"Malipo yako ya kahawa kwa kipindi "
        f"{payment.period_start} - {payment.period_end}: "
        f"KESI {payment.total_amount} "
        f"({payment.total_kg_dry}kg kavu) "
        f"imeingia kwa akaunti yako. "
        f"Status: {payment.get_status_display()}. "
        f"Asante!"
    )
    
    result = send_sms_simulation(farmer.phone, message)
    return result

def send_low_balance_alert(farmer, current_balance, threshold=Decimal('1000.00')):
    """Alert farmer when their account balance is low."""
    message = (
        f"Habari {farmer.name}. "
        f"Akaunti yako ina salio la chini: KES {current_balance}. "
        f"Tafadhali toa kahawa zaidi au wasiliana na ofisi "
        f"kwa maelezo zaidi. Asante."
    )
    
    result = send_sms_simulation(farmer.phone, message)
    return result

def send_daily_summary(farmer, deliveries_today, total_today):
    """Send daily summary to farmer (optional feature)."""
    if deliveries_today == 0:
        message = (
            f"Habari {farmer.name}. "
            f"Hakuna mizigo ya kahawa leo {timezone.now().date()}. "
            f"Kumbuka kuleta kahawa yako kesho. Asante."
        )
    else:
        message = (
            f"Habari {farmer.name}. "
            f"Leo {timezone.now().date()}: "
            f"Mizigo {deliveries_today}, "
            f"Jumla: KES {total_today}. "
            f"Hongera kwa kazi nzuri!"
        )
    
    result = send_sms_simulation(farmer.phone, message)
    return result

def send_welcome_message(farmer):
    """Send welcome SMS when farmer registers."""
    message = (
        f"Karibu {farmer.name} kwenye CoffeeFlow! "
        f"Umeandikishwa kama mkulima wa kahawa. "
        f"Nambari yako: {farmer.farmer_id}. "
        f"Tuma kahawa yako kwenye kituo chochote kilicho na mfumo wetu. "
        f"Utapokea ujumbe baada ya kila mzigo. Asante!"
    )
    
    result = send_sms_simulation(farmer.phone, message)
    return result

# Africa's Talking integration template (for future use)
def send_sms_africas_talking(phone_number, message):
    """
    Real SMS sending via Africa's Talking API.
    Uncomment and configure when ready for production.
    """
    """
    import africastalking
    
    # Initialize SDK
    username = "your_username"  # Use 'sandbox' for test environment
    api_key = "your_api_key"
    africastalking.initialize(username, api_key)
    
    # Initialize SMS service
    sms = africastalking.SMS
    
    try:
        # Send SMS
        response = sms.send(message, [phone_number])
        return {
            "status": "success",
            "message_id": response['SMSMessageData']['Recipients'][0]['messageId'],
            "cost": response['SMSMessageData']['Recipients'][0]['cost']
        }
    except Exception as e:
        logger.error(f"Africa's Talking SMS failed: {e}")
        return {"status": "failed", "error": str(e)}
    """
    pass