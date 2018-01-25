#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import copy
from datetime import datetime
from os.path import basename, abspath, dirname, isfile, join
from fabric.api import env, puts, abort, cd, hide, task
from fabric.operations import sudo, settings, run
from fabric.contrib import console
from fabric.contrib.files import upload_template
from .init_machine import test_configuration, _verify_sudo
from fabric.colors import _wrap_with, green
green_bg = _wrap_with('42')
red_bg = _wrap_with('41')
fabric_utils_path = dirname(abspath(__file__))

@task
def setup_project():
    puts(green_bg('Start setup...'))
    start_time = datetime.now()
    _verify_sudo()
    _create_virtualenv()
    _install_gunicorn()
    _git_clone()
    _install_requirements()
    _upload_nginx_conf()
    _upload_rungunicorn_script()
    _upload_supervisord_conf()
    _prepare_media_path()
    end_time = datetime.now()
    finish_message = '[%s] Correctly finished in %i seconds' % \
    (green_bg(end_time.strftime('%H:%M:%S')), (end_time - start_time).seconds)
    puts(finish_message)




def _install_requirements():
    ''' you must have a file called requirements.txt in your project root'''
    if 'requirements_file' in env and env.requirements_file:
        sudo('chown -R %s /opt/django' % env.login_user)
        sudo('apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev')
        virtenvrun('pip install -r %s' % env.requirements_file)

def _install_gunicorn():
    """ force gunicorn installation into your virtualenv, even if it's installed globally.
    for more details: https://github.com/benoitc/gunicorn/pull/280 """
    virtenvsudo('pip install -I gunicorn')




def _create_virtualenv():
    sudo('virtualenv --python=python3.6 --%s %s' % (' --'.join(env.virtenv_options), env.virtenv))
    sudo('chown -R %s /opt/django' % env.login_user)


def virtenvrun(command):
    export_env = 'export WORKON_HOME=%s;' % join(env.django_user_home, 'envs')
    activate = 'workon %s' % env.project
    run(export_env + 'source /usr/local/bin/virtualenvwrapper.sh;' + activate + ' && ' + command)


def virtenvsudo(command):
    export_env = 'export WORKON_HOME=%s;' % join(env.django_user_home, 'envs')
    activate = 'workon %s' % env.project
    sudo(export_env + 'source /usr/local/bin/virtualenvwrapper.sh;' + activate + ' && ' + command)


def _git_clone():
    sudo('git clone %s %s' % (env.repository, env.code_root))


def _test_nginx_conf():
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('nginx -t -c /etc/nginx/nginx.conf')
    if 'test failed' in res:
        abort(red_bg('NGINX configuration test failed! Please review your parameters.'))


def _upload_nginx_conf():
    ''' upload nginx conf '''
    local_nginx_conf_file_name = 'nginx.conf'
    if env.nginx_https:
        local_nginx_conf_file_name = 'nginx_https.conf'
    local_nginx_conf_file_path = "%s/conf/%s" % (dirname(env.real_fabfile), local_nginx_conf_file_name)
    if isfile(local_nginx_conf_file_path):
        ''' we use user defined conf template '''
        template = local_nginx_conf_file_path
    else:
        template = '%s/conf/%s' % (fabric_utils_path, local_nginx_conf_file_name)
    context = copy(env)
    # Template
    upload_template(template, env.nginx_conf_file,
                    context=context, backup=False, use_sudo=True)

    sudo('ln -sf %s /etc/nginx/sites-enabled/%s' % (env.nginx_conf_file, basename(env.nginx_conf_file)))
    _test_nginx_conf()
    sudo('nginx -s reload')


def _reload_supervisorctl():
    sudo('%(supervisorctl)s reread' % env)
    sudo('%(supervisorctl)s reload' % env)


def _upload_supervisord_conf():
    ''' upload supervisor conf '''
    local_supervisord_conf_file_path = "%s/conf/supervisord.conf" % dirname(env.real_fabfile)
    if isfile(local_supervisord_conf_file_path):
        ''' we use user defined supervisord.conf template '''
        template = local_supervisord_conf_file_path
    else:
        template = '%s/conf/supervisord.conf' % fabric_utils_path
    upload_template(template, env.supervisord_conf_file,
                    context=env, backup=False, use_sudo=True)
    sudo('ln -sf %s /etc/supervisor/conf.d/%s' % (env.supervisord_conf_file, basename(env.supervisord_conf_file)))
    _reload_supervisorctl()


def _prepare_media_path():
    for path in [env.django_media_path, env.django_static_path]:
        path = path.rstrip('/')
        sudo('mkdir -p %s' % path)
        sudo('chmod -R 755 %s' % path)
        sudo('chown -R %s %s' % (env.login_user, path))


def _upload_rungunicorn_script():
    ''' upload rungunicorn conf '''
    if isfile('scripts/rungunicorn.sh'):
        ''' we use user defined rungunicorn file '''
        template = 'scripts/rungunicorn.sh'
    else:
        template = '%s/scripts/rungunicorn.sh' % fabric_utils_path
    context = copy(env)
    upload_template(template, env.rungunicorn_script,
                    context=context, backup=False, use_sudo=True)
    sudo('chmod +x %s' % env.rungunicorn_script)
