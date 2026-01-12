# -*- coding: utf-8 -*- 
import sys 
 
with open('milkflow/settings.py', 'r', encoding='utf-8') as f: 
    lines = f.readlines() 
 
print('Checking imports...') 
 
for i, line in enumerate(lines[:15]): 
    if 'import' in line.lower(): 
        print(f'Line {i+1}: {line.rstrip()}') 
 
# Check for os import 
has_os = any('import os' in line or 'from os' in line for line in lines) 
if has_os: 
    print('û os module is imported') 
else: 
    print('? os module is NOT imported') 
