
from fabric.api import *

# Hosts to deploy onto
env.hosts = ['localhost']

# Where your project code lives on the server
env.project_root = 'G:\Jerome (F)\Hotarubi\hotarubi.touhead.com'


def deploy_static():
    with cd(env.project_root):
        run('./manage.py collectstatic -v0 --noinput')