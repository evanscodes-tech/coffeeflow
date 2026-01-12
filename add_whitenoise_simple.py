# Add WhiteNoise middleware 
 
with open('milkflow/settings.py', 'r') as f: 
    lines = f.readlines() 
 
# Find MIDDLEWARE list 
new_lines = [] 
whitenoise_added = False 
 
for line in lines: 
    # Add WhiteNoise after SecurityMiddleware 
    if 'SecurityMiddleware' in line and not whitenoise_added: 
        new_lines.append(line) 
        new_lines.append("    'whitenoise.middleware.WhiteNoiseMiddleware',\n") 
        whitenoise_added = True 
    else: 
        new_lines.append(line) 
 
# Write back 
with open('milkflow/settings.py', 'w') as f: 
    f.writelines(new_lines) 
 
print('WhiteNoise middleware added') 
