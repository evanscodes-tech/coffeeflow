from django.contrib import admin 
from django.urls import path, include 
from core.views import dashboard 
from django.contrib.auth import views as auth_views 
from django.views.generic import RedirectView

from core.views import register_collector, register_farmer
 
urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('api/', include('core.urls')), 
    path('dashboard/', dashboard, name='dashboard'), 
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'), 
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 
     path('', RedirectView.as_view(pattern_name='login'), name='home'),
     
      path('register/collector/', register_collector, name='register_collector'),
    path('register/farmer/', register_farmer, name='register_farmer'),
] 
