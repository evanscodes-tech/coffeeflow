import os 
 
# Read settings 
with open('milkflow/settings.py', 'r') as f: 
    lines = f.readlines() 
 
# Find where to add STATIC_ROOT (look for STATIC_URL) 
new_lines = [] 
static_added = False 
 
for line in lines: 
    # If we find STATIC_URL line, add STATIC_ROOT after it 
    if 'STATIC_URL' in line and not static_added: 
        new_lines.append(line) 
        new_lines.append('STATIC_ROOT = os.path.join(BASE_DIR, \'staticfiles\')\n') 
        static_added = True 
    else: 
        new_lines.append(line) 
 
# If STATIC_URL wasn't found, add both 
if not static_added: 
    # Find a good place (after BASE_DIR definition) 
    for i, line in enumerate(new_lines): 
        if 'BASE_DIR =' in line: 
            new_lines.insert(i+2, '\n# Static files\n') 
            new_lines.insert(i+3, 'STATIC_URL = \'static/\'\n') 
            new_lines.insert(i+4, 'STATIC_ROOT = os.path.join(BASE_DIR, \'staticfiles\')\n') 
            break 
 
# Write back 
with open('milkflow/settings.py', 'w') as f: 
    f.writelines(new_lines) 
 
print('Static files configuration added') 
