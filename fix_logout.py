# Fix logout view 
 
with open('milkflow/urls.py', 'r') as f: 
    content = f.read() 
 
# Update logout line 
new_content = content.replace( 
    "path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),", 
    "path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html', next_page='/'), name='logout')," 
) 
 
with open('milkflow/urls.py', 'w') as f: 
    f.write(new_content) 
 
print('Updated logout view') 
