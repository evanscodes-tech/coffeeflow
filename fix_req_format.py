# Fix requirements.txt formatting 
import re 
 
# Read the file 
with open('requirements.txt', 'r') as f: 
    content = f.read() 
 
# Fix the \\n issue - split lines properly 
lines = [] 
for line in content.split('\\n'):  # Fix escaped newlines 
    line = line.strip() 
    if line and '\\\\n' not in line:  # Remove bad lines 
        lines.append(line) 
 
# Also fix any actual newline issues 
clean_lines = [] 
for line in lines: 
    # Split if multiple packages on one line 
    if ' ' in line and '==' in line: 
        parts = re.split(r'\\s+', line) 
        clean_lines.extend([p for p in parts if '==' in p]) 
    else: 
        clean_lines.append(line) 
 
# Ensure Railway packages are present 
railway_pkgs = ['dj-database-url==2.3.0', 'gunicorn==21.2.0', 'psycopg2-binary==2.9.9', 'whitenoise==6.6.0'] 
for pkg in railway_pkgs: 
    if not any(pkg in line for line in clean_lines): 
        clean_lines.append(pkg) 
 
# Write back 
with open('requirements.txt', 'w') as f: 
    f.write('\\n'.join(clean_lines)) 
 
print(f'Fixed requirements.txt: {len(clean_lines)} packages') 
print('Last 5 lines:') 
for line in clean_lines[-5:]: 
    print(f'  {line}') 
