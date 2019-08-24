# -*-coding:utf-8 -*-
import os

from fabric.api import run, env, roles, prefix, put, cd
from fabric.contrib.files import exists

env.roledefs = {
    'develop': [
        'jummy@111.230.25.51',
    ],
}

ENV_PATH = '/home/jummy/workspace/blog-env'
ACTIVE_FILE_PATH = os.path.join(ENV_PATH, 'bin/activate')
PYPI_INDEX = 'http://111.230.25.51:8080/simple/'


def pip(package, version=None):
    command = 'pip install -i {pypi} --trusted-host=111.230.25.51 '.format(pypi=PYPI_INDEX)
    if version:
        command = command + '{package}=={version}'.format(package=package, version=version)
    else:
        command = command + package
    run(command)


@roles('develop')
def deploy(version):
    ensure_venv()

    install(version)

    upload_env()

    upload_supervisord_conf()

    run_supervisord()


def install(version):
    with prefix('source %s' % ACTIVE_FILE_PATH):
        pip('typeidea', version)


# 创建虚拟环境
def ensure_venv():
    if not exists(ACTIVE_FILE_PATH):
        run('virtualenv {}'.format(ENV_PATH))


def ensure_supervisord():
    with prefix('source %s' % ACTIVE_FILE_PATH):
        result = run('which supervisord', warn_only=True)
        if 'no supervisord' in result:
            pip('supervisor')


def upload_env():
    put('typeidea/.env', '{}/.env'.format(ENV_PATH))


def upload_supervisord_conf():
    put('conf/supervisord.conf', '{}/supervisord.conf'.format(ENV_PATH))


def run_supervisord():
    ensure_supervisord()

    result = run('ps aux|grep supervisord | grep -v grep', warn_only=True)
    if result:
        shutdown_supervisord()
        # return restart_supervisord()

    with prefix('source %s' % ACTIVE_FILE_PATH):
        with cd(ENV_PATH):
            run('supervisord -c supervisord.conf')


def restart_supervisord():
    with prefix('source %s' % ACTIVE_FILE_PATH):
        with cd(ENV_PATH):
            run('supervisorctl -c supervisord.conf restart all')


def shutdown_supervisord():
    with prefix('source %s' % ACTIVE_FILE_PATH):
        with cd(ENV_PATH):
            run('supervisorctl -c supervisord.conf shutdown')