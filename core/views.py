from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db.models import Sum, Count
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Farmer, Delivery, Payment
from .serializers import FarmerSerializer, DeliverySerializer, PaymentSerializer


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import login

# ViewSets
class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all().order_by('-delivery_time')
    serializer_class = DeliverySerializer
    
    @action(detail=False, methods=['post'])
    def record_delivery(self, request):
        """Endpoint for hardware (scale) to send delivery data."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-period_end')
    serializer_class = PaymentSerializer

# Report API Functions
@api_view(['GET'])
@permission_classes([AllowAny])
def daily_summary(request):
    """Get daily summary for a specific date or today."""
    date_str = request.GET.get('date')
    
    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    else:
        target_date = timezone.now().date()
    
    deliveries = Delivery.objects.filter(delivery_time__date=target_date)
    
    summary = deliveries.aggregate(
        total_deliveries=Count('id'),
        total_cherry_kg=Sum('cherry_kg'),  # CHANGED
        total_kg_dry=Sum('kg_dry'),        # CHANGED
        total_amount=Sum('total_amount')
    )
    
    farmers_count = deliveries.values('farmer').distinct().count()
    
    return Response({
        'date': str(target_date),
        'total_deliveries': summary['total_deliveries'] or 0,
        'total_cherry_kg': float(summary['total_cherry_kg'] or 0),  # CHANGED
        'total_kg_dry': float(summary['total_kg_dry'] or 0),        # CHANGED
        'total_amount': float(summary['total_amount'] or 0),
        'farmers_count': farmers_count
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def farmer_history(request, farmer_id):
    """Get delivery history for a specific farmer."""
    try:
        farmer = Farmer.objects.get(id=farmer_id)
    except Farmer.DoesNotExist:
        return Response({'error': 'Farmer not found'}, status=404)
    
    deliveries = farmer.deliveries.all().order_by('-delivery_time')
    
    totals = deliveries.aggregate(
        total_deliveries=Count('id'),
        total_cherry_kg=Sum('cherry_kg'),  # CHANGED
        total_kg_dry=Sum('kg_dry'),        # CHANGED
        total_amount=Sum('total_amount')
    )
    
    delivery_data = DeliverySerializer(deliveries[:50], many=True).data
    
    return Response({
        'farmer': {
            'id': farmer.id,
            'name': farmer.name,
            'phone': farmer.phone,
            'location': farmer.location
        },
        'totals': {
            'total_deliveries': totals['total_deliveries'] or 0,
            'total_cherry_kg': float(totals['total_cherry_kg'] or 0),  # CHANGED
            'total_kg_dry': float(totals['total_kg_dry'] or 0),        # CHANGED
            'total_amount': float(totals['total_amount'] or 0)
        },
        'recent_deliveries': delivery_data
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def period_report(request):
    """Get report for a date range (default: last 7 days)."""
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    
    if request.GET.get('start_date'):
        try:
            start_date = datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if request.GET.get('end_date'):
        try:
            end_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date()
        except ValueError:
            pass
    
    deliveries = Delivery.objects.filter(
        delivery_time__date__range=[start_date, end_date]
    )
    
    daily_data = []
    current_date = start_date
    while current_date <= end_date:
        day_deliveries = deliveries.filter(delivery_time__date=current_date)
        day_totals = day_deliveries.aggregate(
            deliveries=Count('id'),
            cherry_kg=Sum('cherry_kg'),  # CHANGED
            kg_dry=Sum('kg_dry'),        # CHANGED
            amount=Sum('total_amount')
        )
        
        daily_data.append({
            'date': str(current_date),
            'deliveries': day_totals['deliveries'] or 0,
            'cherry_kg': float(day_totals['cherry_kg'] or 0),  # CHANGED
            'kg_dry': float(day_totals['kg_dry'] or 0),        # CHANGED
            'amount': float(day_totals['amount'] or 0)
        })
        current_date += timedelta(days=1)
    
    totals = deliveries.aggregate(
        total_deliveries=Count('id'),
        total_cherry_kg=Sum('cherry_kg'),  # CHANGED
        total_kg_dry=Sum('kg_dry'),        # CHANGED
        total_amount=Sum('total_amount')
    )
    
    return Response({
        'period': {
            'start_date': str(start_date),
            'end_date': str(end_date),
            'days': (end_date - start_date).days + 1
        },
        'totals': {
            'total_deliveries': totals['total_deliveries'] or 0,
            'total_cherry_kg': float(totals['total_cherry_kg'] or 0),  # CHANGED
            'total_kg_dry': float(totals['total_kg_dry'] or 0),        # CHANGED
            'total_amount': float(totals['total_amount'] or 0)
        },
        'daily_breakdown': daily_data
    })

# Dashboard View
@login_required
def dashboard(request):
    """Main dashboard view."""
    # Get today's summary
    today = timezone.now().date()
    today_deliveries = Delivery.objects.filter(delivery_time__date=today)
    
    today_summary = today_deliveries.aggregate(
        deliveries=Count('id'),
        cherry_kg=Sum('cherry_kg'),  # CHANGED
        kg_dry=Sum('kg_dry'),        # CHANGED
        amount=Sum('total_amount')
    )
    
    # Get recent deliveries (last 10)
    recent_deliveries = Delivery.objects.all().order_by('-delivery_time')[:10]
    
    # Get top farmers (by cherry_kg today)
    top_farmers_today = Farmer.objects.filter(
        deliveries__delivery_time__date=today
    ).annotate(
        today_cherry_kg=Sum('deliveries__cherry_kg')  # CHANGED
    ).order_by('-today_cherry_kg')[:5]
    
    # Get SMS stats
    sms_stats = {
        'sent': Delivery.objects.filter(sms_sent=True).count(),
        'total': Delivery.objects.count(),
        'failed': Delivery.objects.filter(sms_status='failed').count()
    }
    
    context = {
        'today': today,
        'today_summary': {
            'deliveries': today_summary['deliveries'] or 0,
            'cherry_kg': float(today_summary['cherry_kg'] or 0),  # CHANGED
            'kg_dry': float(today_summary['kg_dry'] or 0),        # CHANGED
            'amount': float(today_summary['amount'] or 0),
        },
        'recent_deliveries': recent_deliveries,
        'top_farmers_today': top_farmers_today,
        'sms_stats': sms_stats,
        'total_farmers': Farmer.objects.count(),
        'total_deliveries': Delivery.objects.count(),
    }
    return render(request, 'core/dashboard.html', context)





# In core/views.py


def register_collector(request):
    """Register new coffee collector account"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add to Collectors group
            collectors_group, created = Group.objects.get_or_create(name='Collectors')
            user.groups.add(collectors_group)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register_collector.html', {'form': form})

def register_farmer(request):
    """Register coffee farmer (with additional info later)"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add to Farmers group
            farmers_group, created = Group.objects.get_or_create(name='Farmers')
            user.groups.add(farmers_group)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register_farmer.html', {'form': form})