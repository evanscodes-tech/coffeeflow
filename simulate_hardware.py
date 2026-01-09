import requests
import random
import time

API_URL = "http://localhost:8000/api/deliveries/"

def send_delivery(farmer_id, cherry_kg):
    """Simulate coffee cherry delivery from hardware scale."""
    data = {
        "farmer": farmer_id,
        "cherry_kg": str(cherry_kg),  # CHANGED: weight_kg → cherry_kg
        "recorded_by": f"COFFEE_SCALE_{random.randint(1, 5)}"  # Updated scale name
    }
    
    try:
        response = requests.post(API_URL, json=data, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            resp_data = response.json()
            print(f"  ✅ Coffee Delivery Recorded!")
            print(f"     Cherry: {cherry_kg}kg → Dry: {resp_data.get('kg_dry')}kg")
            print(f"     Amount: KES {resp_data.get('total_amount')}")
            print(f"     SMS Status: {resp_data.get('sms_status', 'Not sent')}")
        else:
            print(f"  ❌ Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"  🔌 ERROR: Cannot connect to server. Is CoffeeFlow running?")
        print(f"     Run: python manage.py runserver")
    except Exception as e:
        print(f"  ⚠️ ERROR: {e}")

def simulate_coffee_season():
    """Simulate a coffee harvesting season with varying deliveries."""
    print("=" * 60)
    print("☕ COFFEEFLOW HARDWARE SIMULATION")
    print("Simulating coffee cherry deliveries from digital scales")
    print("=" * 60)
    
    farmer_id = 1  # Change to your farmer's ID
    
    # Different coffee delivery scenarios
    scenarios = [
        {"name": "Small farmer", "min": 5, "max": 15},
        {"name": "Medium farmer", "min": 15, "max": 30},
        {"name": "Large farmer", "min": 25, "max": 50},
        {"name": "Bulk delivery", "min": 40, "max": 80},
    ]
    
    print(f"\nSimulating deliveries for Farmer ID: {farmer_id}")
    print("Each delivery will be automatically converted to dry weight (20% yield)")
    print("SMS notifications will be sent to farmer after each delivery\n")
    
    for i in range(8):  # Simulate 8 deliveries
        scenario = random.choice(scenarios)
        cherry_weight = round(random.uniform(scenario["min"], scenario["max"]), 2)
        
        print(f"\n[{i+1}] {scenario['name']}: {cherry_weight}kg coffee cherries")
        print("-" * 40)
        
        send_delivery(farmer_id, cherry_weight)
        
        # Random delay between deliveries (1-4 seconds)
        if i < 7:  # Don't wait after last delivery
            delay = random.uniform(1, 4)
            print(f"    Waiting {delay:.1f}s for next delivery...")
            time.sleep(delay)
    
    print("\n" + "=" * 60)
    print("✅ SIMULATION COMPLETE")
    print(f"Check dashboard: http://localhost:8000/dashboard/")
    print(f"Check admin: http://localhost:8000/admin/core/delivery/")
    print("=" * 60)

def test_single_delivery():
    """Test a single delivery for debugging."""
    print("🧪 Testing single coffee delivery...")
    send_delivery(farmer_id=1, cherry_kg=25.75)
    print("\nTest complete. Check database and SMS logs.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='CoffeeFlow Hardware Simulator')
    parser.add_argument('--test', action='store_true', help='Test single delivery')
    parser.add_argument('--farmer', type=int, default=1, help='Farmer ID (default: 1)')
    parser.add_argument('--weight', type=float, help='Specific cherry weight in kg')
    
    args = parser.parse_args()
    
    if args.test:
        test_single_delivery()
    elif args.weight:
        print(f"📦 Sending specific delivery: {args.weight}kg coffee cherries")
        send_delivery(args.farmer, args.weight)
    else:
        simulate_coffee_season()