# ☕ CoffeeFlow - Digital Coffee Collection System

**Automated coffee cherry weighing, farmer payments, SMS notifications, and real-time reporting for coffee cooperatives in Kenya.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Live Demo
- **Dashboard:** [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
- **Admin Panel:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **API Documentation:** [http://localhost:8000/api/](http://localhost:8000/api/)

*Default credentials: admin / admin123*

## ✨ Features

### 🌱 Coffee-Specific Operations
- **Automatic Conversion:** 5kg cherry coffee → 1kg dry coffee (20% yield)
- **Dynamic Pricing:** Configurable price per kg dry coffee (default: KES 120/kg)
- **Farmer Management:** Register farmers with IDs, locations, contact info

### 📱 Real-Time Notifications
- **Instant SMS:** Farmers receive confirmation after each delivery
- **Kiswahili Messages:** Localized communication for better understanding
- **SMS Status Tracking:** Monitor delivery confirmation status

### 📊 Dashboard & Reporting
- **Live Statistics:** Today's cherry weight, dry weight, total value
- **Farmer History:** Individual delivery history and totals
- **Period Reports:** Daily, weekly, monthly breakdowns
- **Export Data:** CSV export for accounting

### ⚙️ Hardware Integration Ready
- **Scale Integration:** Connect digital scales via ESP32/HX711
- **API Endpoints:** REST API for hardware communication
- **Simulation Tool:** Test without physical hardware

### 👨‍💼 Admin Management
- **User-Friendly Admin:** Django admin with custom enhancements
- **SMS Management:** Resend failed notifications
- **Data Validation:** Prevent duplicate entries and errors

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows 10/11, macOS, or Linux
- 100MB free disk space

### Installation (5 Minutes)

#### Option A: One-Click Installer (Windows)
1. Download `CoffeeFlow_Setup.exe`
2. Run installer and follow prompts
3. Launch CoffeeFlow from Start Menu

#### Option B: Manual Installation
```bash
# 1. Clone repository
git clone https://github.com/evanscodes-tech/coffeeflow.git
cd coffeeflow

# 2. Run setup script
setup.bat  # Windows
./setup.sh # Linux/macOS

# 3. Start server
start_coffeeflow.bat  # Windows
./start_coffeeflow.sh # Linux/macOS