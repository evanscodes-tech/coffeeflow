# Fix Railway requirements 
import re 
 
# Read current requirements 
with open('requirements.txt', 'r') as f: 
    lines = f.readlines() 
 
# Remove Windows-only packages 
new_lines = [] 
windows_packages = ['pywin32', 'pywinpty'] 
for line in lines: 
    if not any(wp in line for wp in windows_packages): 
        new_lines.append(line) 
 
# Add Railway-specific packages 
railway_packages = [ 
    'dj-database-url==2.3.0', 
    'gunicorn==21.2.0', 
    'psycopg2-binary==2.9.9', 
    'whitenoise==6.6.0', 
] 
 
for pkg in railway_packages: 
    new_lines.append(pkg + '\\n') 
 
# Write back 
with open('requirements.txt', 'w') as f: 
    f.writelines(new_lines) 
 
print('Fixed requirements.txt for Railway') 
print('Removed pywin32, pywinpty (Windows-only)') 
print('Added Railway packages') 
