print("Quick check of updated settings:") 
with open('milkflow/settings.py', 'r') as f: 
    for line in f: 
        if 'DEBUG' in line or 'SECRET_KEY' in line or 'ALLOWED_HOSTS' in line or 'decouple' in line: 
            print(line.rstrip()) 
