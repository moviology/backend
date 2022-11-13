import multiprocessing
import os
from distutils.util import strtobool

dev = os.environ.get("SERVER_ENV", "production") == "development"

workers = dev and 1 or multiprocessing.cpu_count() * 2 + 1
bind = ':5000'
umask = 0o007
reload = dev
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'