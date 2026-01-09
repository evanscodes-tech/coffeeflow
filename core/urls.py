from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FarmerViewSet, 
    DeliveryViewSet, 
    PaymentViewSet,
    daily_summary, 
    farmer_history, 
    period_report
)

router = DefaultRouter()
router.register(r'farmers', FarmerViewSet)
router.register(r'deliveries', DeliveryViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reports/daily/', daily_summary, name='daily-summary'),
    path('reports/farmer/<int:farmer_id>/history/', farmer_history, name='farmer-history'),
    path('reports/period/', period_report, name='period-report'),
]