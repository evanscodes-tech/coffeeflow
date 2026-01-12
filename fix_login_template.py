# Fix login template issue 
 
with open('milkflow/urls.py', 'r') as f: 
    content = f.read() 
 
# Replace the login line 
new_content = content.replace( 
    "path('accounts/login/', auth_views.LoginView.as_view(), name='login'),", 
    "path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login')," 
) 
 
with open('milkflow/urls.py', 'w') as f: 
    f.write(new_content) 
 
print('Updated login view to use admin template') 
