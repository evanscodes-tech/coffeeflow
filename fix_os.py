# -*- coding: utf-8 -*- 
 
with open('milkflow/settings.py', 'r', encoding='utf-8') as f: 
    lines = f.readlines() 
 
# Check if os is imported 
os_imported = False 
for line in lines: 
    if 'import os' in line or 'from os' in line: 
        os_imported = True 
        break 
 
if os_imported: 
    print('os is already imported') 
else: 
    # Add import at the top 
    new_lines = [] 
    for line in lines: 
        if line.strip() and not line.startswith(('#', 'import ', 'from ')): 
            new_lines.append('import os\n') 
            new_lines.append(line) 
            break 
        new_lines.append(line) 
    # Add remaining lines 
    for line in lines[len(new_lines)-1:]: 
        new_lines.append(line) 
 
    # Write back 
    with open('milkflow/settings.py', 'w', encoding='utf-8') as f: 
        f.writelines(new_lines) 
    print('Added import os to settings.py') 
