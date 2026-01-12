 
with open('milkflow/settings.py', 'r') as f: 
    content = f.read() 
 
if 'STATIC_ROOT' in content: 
    print('STATIC_ROOT already exists in settings') 
else: 
    print('STATIC_ROOT not found - will add it') 
