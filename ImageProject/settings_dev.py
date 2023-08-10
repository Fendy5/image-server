# 开发环境的设置
from ImageProject.settings import BASE_DIR

print('dev~')
DEBUG = True
ALLOWED_HOSTS = ['*']
BASE_URL = 'http://localhost:8000'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
