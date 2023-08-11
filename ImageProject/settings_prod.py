# 生产环境的设置
import os

import pymysql

from ImageProject.settings import BASE_DIR
from ImageProject.views import get_today

print('prod~')
DEBUG = False
# 使用pymysql代替mysqlclient
pymysql.install_as_MySQLdb()

ALLOWED_HOSTS = [
    'image.fendy5.cn',
    '172.17.0.1'
]

LOG_ROOT = os.path.join(BASE_DIR, 'logs')  # 根据项目结构设置日志存储路径

if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, get_today() + '.log'),
            'when': 'midnight',  # 每天生成一个新的日志文件
            'backupCount': 7,  # 保留最近7天的日志文件
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'tool': {  # Django应用程序的名称
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'image',
        'USER': 'image',
        'PASSWORD': 'Meij4X27aC6PDtcd',
        'HOST': '172.42.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET time_zone='Asia/Shanghai';",  # 设置为 'Asia/Shanghai'
        },
    },
}
