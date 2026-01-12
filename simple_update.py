# Simple settings updater 
import sys 
 
print("Reading settings.py...") 
with open('milkflow/settings.py', 'r') as f: 
    lines = f.readlines() 
 
# Backup original 
with open('milkflow/settings_backup.py', 'w') as f: 
    f.writelines(lines) 
print("Backup created: milkflow/settings_backup.py") 
 
# Process each line 
new_lines = [] 
decouple_added = False 
 
for line in lines: 
    stripped = line.strip() 
 
    # Add decouple import after other imports 
    if not decouple_added and stripped and not stripped.startswith(('import ', 'from ')): 
        new_lines.append('from decouple import config\n\n') 
        decouple_added = True 
 
    # Update DEBUG 
    if stripped.startswith('DEBUG ='): 
        new_lines.append("DEBUG = config('DEBUG', default=False, cast=bool)\n") 
        continue 
 
    # Update SECRET_KEY 
    if stripped.startswith('SECRET_KEY ='): 
        new_lines.append("SECRET_KEY = config('SECRET_KEY')\n") 
        continue 
 
    # Update ALLOWED_HOSTS 
    if stripped.startswith('ALLOWED_HOSTS ='): 
        new_lines.append("ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')\n") 
        continue 
 
    # Keep other lines as-is 
    new_lines.append(line) 
 
# Write updated file 
with open('milkflow/settings.py', 'w') as f: 
    f.writelines(new_lines) 
 
print("Settings updated successfully!") 
