# Production settings - add to your settings.py 
 
# Security 
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool) 
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=0, cast=int) 
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False, cast=bool) 
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=False, cast=bool) 
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool) 
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool) 
 
# Static files with WhiteNoise 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 
