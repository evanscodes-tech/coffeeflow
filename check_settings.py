import re 
 
print("Checking your settings.py file...") 
 
with open('milkflow/settings.py', 'r') as f: 
    content = f.read() 
 
# Find the key lines 
debug_match = re.search(r'DEBUG\s*=\s*.*', content) 
secret_match = re.search(r'SECRET_KEY\s*=\s*.*', content) 
hosts_match = re.search(r'ALLOWED_HOSTS\s*=\s*.*', content) 
 
print("1. DEBUG line:", debug_match.group(0) if debug_match else "Not found") 
print("2. SECRET_KEY line:", secret_match.group(0) if secret_match else "Not found") 
print("3. ALLOWED_HOSTS line:", hosts_match.group(0) if hosts_match else "Not found") 
