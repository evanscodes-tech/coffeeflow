# Add production security settings 
 
with open('milkflow/settings.py', 'a') as f: 
    f.write('\\n\\n# Production security settings\\n') 
    f.write('DEBUG = config(\\'DEBUG\\', default=False, cast=bool)\\n\\n') 
    f.write('# Force secure settings when DEBUG=False\\n') 
    f.write('if not DEBUG:\\n') 
    f.write('    SECURE_SSL_REDIRECT = True\\n') 
    f.write('    SESSION_COOKIE_SECURE = True\\n') 
    f.write('    CSRF_COOKIE_SECURE = True\\n') 
    f.write('    SECURE_BROWSER_XSS_FILTER = True\\n') 
    f.write('    SECURE_CONTENT_TYPE_NOSNIFF = True\\n') 
    f.write('    SECURE_HSTS_SECONDS = 31536000  # 1 year\\n') 
    f.write('    SECURE_HSTS_INCLUDE_SUBDOMAINS = True\\n') 
    f.write('    SECURE_HSTS_PRELOAD = True\\n') 
 
print('Added production security settings to settings.py') 
