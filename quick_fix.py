# Quick fix for settings.py 
 
# Read the file 
with open('milkflow/settings.py', 'r', encoding='utf-8') as f: 
    content = f.read() 
 
# Add import os at the very beginning if not present 
if 'import os' not in content and 'from os' not in content: 
    lines = content.split('\n') 
    # Find first non-import line 
    for i, line in enumerate(lines): 
        if line.strip() and not line.startswith(('import ', 'from ')): 
            lines.insert(i, 'import os') 
            break 
    content = '\n'.join(lines) 
 
# Write back 
with open('milkflow/settings.py', 'w', encoding='utf-8') as f: 
    f.write(content) 
 
print('Fixed settings.py') 
