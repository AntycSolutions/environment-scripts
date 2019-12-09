# generates an apache site config file

from distutils import version

try:
    import settings
    default_user = settings.USER
    default_email = settings.EMAIL
except ImportError:
    default_user = ''
    default_email = ''


def create_config(
    url=None,
    git_dir=None,
    proj_dir=None,
    wsgi_dir=None,
    url_dir=None,
    venv=None,
    user=None,
    favicon=None,
    python_ver=None,
    server_alias=None,
    email=None,
    ssl=None,
    ssl_certificate_file=None,
    ssl_certificate_key_file=None,
    server_alias_https=None,
    hsts_domains=None,
    filename=None,
    create_file=True,
):
    # args could be in an OrderedDict
    print('\n* Required args *\n')

    if not url:
        print('url: ', end='')
        url = input()
        if not url:
            raise Exception('Enter an url')

    if not git_dir:
        print('git_dir: ', end='')
        git_dir = input()
        if not git_dir:
            raise Exception('Enter a git_dir')

    print('\n* Optional args (leave blank to use defaults) *\n')

    if not proj_dir and proj_dir is not False:
        print((
            'proj_dir (containing Django proj) '
            '(leave blank if your git_dir contains your Django proj): '
        ), end='')
        proj_dir = input()

    default_wsgi_dir = proj_dir or git_dir
    if not wsgi_dir and wsgi_dir is not False:
        print((
            'wsgi_dir (containing wsgi.py) (default is ' +
            default_wsgi_dir +
            '): '
        ), end='')
        wsgi_dir = input()
    if not wsgi_dir:
        wsgi_dir = default_wsgi_dir

    # we can't put the / in the template because we need to support blank value
    if proj_dir:
        proj_dir = '/' + proj_dir

    default_url_dir = 'public_html'
    if not url_dir and url_dir is not False:
        print('url_dir (default is ' + default_url_dir + '): ', end='')
        url_dir = input()
    if not url_dir:
        url_dir = default_url_dir

    default_venv = 'venv_' + wsgi_dir
    if not venv and venv is not False:
        print('venv (default is ' + default_venv + '): ', end='')
        venv = input()
    if not venv:
        venv = default_venv

    if not user and user is not False:
        print('user (default is ' + default_user + '): ', end='')
        user = input()
    if not user:
        if not default_user:
            raise Exception('user required')
        user = default_user

    if not favicon and favicon is not False:
        print('favicon (leave blank to disable): ', end='')
        favicon = input()

    default_python_ver = '3.5'
    if not python_ver and python_ver is not False:
        print('python_ver (default is ' + default_python_ver + '): ', end='')
        python_ver = input()
    if not python_ver:
        python_ver = default_python_ver

    if not server_alias and server_alias is not False:
        print('server_alias (leave blank to disable): ', end='')
        server_alias = input()

    if not email and email is not False:
        print('email (default is ' + default_email + '): ', end='')
        email = input()
    if not email:
        if not default_email:
            raise Exception('email required')
        email = default_email

    if not ssl and ssl is not False:
        print('ssl (enter [y]es or leave blank to disable): ', end='')
        ssl = input().lower()

    if ssl in ['y', 'yes', True]:
        print('\n* Required ssl args *\n')

        if not ssl_certificate_file:
            print('ssl_certificate_file (full path): ', end='')
            ssl_certificate_file = input()
            if not ssl_certificate_file:
                exit('Enter a ssl_certificate_file')

        if not ssl_certificate_key_file:
            print('ssl_certificate_key_file (full path): ', end='')
            ssl_certificate_key_file = input()
            if not ssl_certificate_key_file:
                exit('Enter a ssl_certificate_key_file')

        print('\n* Optional ssl args (leave blank to use defaults) *\n')

        if not server_alias_https and server_alias_https is not False:
            if server_alias:
                msg = 'default is ' + server_alias
            else:
                msg = 'leave blank to disable'
            print('server_alias_https (' + msg + '): ', end='')
            server_alias_https = input()

        if not hsts_domains and hsts_domains is not False:
            print('hsts_domains (leave blank to disable): ', end='')
            hsts_domains = input()

    # Could be moved to a text file
    apache_template = '''\
<VirtualHost *:80>
    # MIME-Type sniffing
    Header set X-Content-Type-Options: nosniff

    # for Require host
    SetEnvIfNoCase Host <escaped_url> VALID_HOST

    ServerName <url>
    <server_alias_opt>ServerAlias <server_alias>
    ServerAdmin <email>

    <favicon_opt>Alias /favicon.ico /home/<user>/<url_dir>/<url>/<git_dir><proj_dir>/static/<favicon>

    Alias /media/ /home/<user>/<url_dir>/<url>/<git_dir><proj_dir>/media/
    Alias /static/ /home/<user>/<url_dir>/<url>/<git_dir><proj_dir>/static/

    <Directory /home/<user>/<url_dir>/<url>/<git_dir><proj_dir>/static>
        <RequireAll>
            Require all granted
            Require env VALID_HOST
        </RequireAll>
    </Directory>
    <Directory /home/<user>/<url_dir>/<url>/<git_dir><proj_dir>/media>
        <RequireAll>
            Require all granted
            Require env VALID_HOST
        </RequireAll>
    </Directory>

    WSGIScriptAlias / /home/<user>/<url_dir>/<url>/<git_dir><proj_dir>/<wsgi_dir>/wsgi.py
    WSGIDaemonProcess <url> <wsgi_daemon_process>
    WSGIProcessGroup <url>

    <Directory /home/<user>/<url_dir>/<url>/<git_dir><proj_dir>/<wsgi_dir>>
        <Files wsgi.py>
            <RequireAll>
                Require all granted
                Require env VALID_HOST
            </RequireAll>
        </Files>
    </Directory>
</Virtualhost>
'''  # noqa E501

    apache_ssl_template = apache_template.replace('<VirtualHost *:80>', '''\
<VirtualHost *:80>
    ServerName <url>
    <server_alias_http_opt>ServerAlias <server_alias_http>
    ServerAdmin <email>

    # Do not use permanent!
    Redirect / https://<url>/
</VirtualHost>

<VirtualHost *:443>
    # SSL
    SSLEngine on

    SSLCertificateFile <ssl_certificate_file>
    SSLCertificateKeyFile <ssl_certificate_key_file>

    # HSTS
    Header always set Strict-Transport-Security "max-age=15768000"

    # Wildcard subdomain redirect
    RewriteEngine On
    RewriteCond %{HTTP_HOST} ^(.*)\.<escaped_url> <or>
    <escaped_url_rewrite_conds>
    RewriteCond %{HTTPS} =on
    # Do not use permanent!
    RewriteRule (.*) https://<url>/ [R,L]

    # Content Security Policy
    <hsts_opt>Header set Content-Security-Policy "script-src 'self' <hsts_domains>
'''  # noqa E501
)

    python34_wsgi_daemon_process_template = '''\
python-path=/home/<user>/<url_dir>/<url>/<git_dir><proj_dir>:/home/<user>/<url_dir>/<url>/<venv>/lib/python<python_ver>/site-packages\
'''  # noqa E501

    python35_wsgi_daemon_process_template = '''\
python-path=/home/<user>/<url_dir>/<url>/<git_dir><proj_dir> python-home=/home/<user>/<url_dir>/<url>/<venv>\
'''  # noqa E501

    if ssl in ['y', 'yes', True]:
        conf = apache_ssl_template

        conf = conf.replace(
            '<ssl_certificate_file>', ssl_certificate_file
        ).replace(
            '<ssl_certificate_key_file>', ssl_certificate_key_file
        )

        if hsts_domains:
            conf = conf.replace(
                '<hsts_domains>', hsts_domains
            ).replace(
                '<hsts_opt>', ''
            )
        else:
            conf = conf.replace('<hsts_opt>', '#')

        if server_alias:
            escaped_url_rewrite_conds = ''
            server_aliases = server_alias.split()
            server_aliases_len = len(server_aliases) - 1
            counter = 0
            skipped = 0
            for alias in server_aliases:
                if alias.endswith(url):
                    skipped += 1
                    continue

                escaped_url_rewrite_cond = (
                    'RewriteCond %{{HTTP_HOST}} ^{}'.format(
                        alias.replace('.', '\.')
                    )
                )
                if counter > 0:
                    escaped_url_rewrite_cond = '    {}'.format(
                        escaped_url_rewrite_cond
                    )
                if counter < (server_aliases_len - skipped):
                    escaped_url_rewrite_cond += ' [OR]\n'

                counter += 1
                escaped_url_rewrite_conds += escaped_url_rewrite_cond

            if counter > 0:
                conf = conf.replace(
                    '<or>', '[OR]'
                ).replace(
                    '<escaped_url_rewrite_conds>', escaped_url_rewrite_conds
                )
            else:
                conf = conf.replace(
                    ' <or>', ''
                ).replace(
                    '<escaped_url_rewrite_conds>', '#'
                )
        else:
            conf = conf.replace(
                ' <or>', ''
            ).replace(
                '<escaped_url_rewrite_conds>', '#'
            )

        if server_alias:
            conf = conf.replace(
                '<server_alias_http>', server_alias
            ).replace(
                '<server_alias_http_opt>', ''
            )
        else:
            conf = conf.replace('<server_alias_http_opt>', '#')

        if server_alias_https or server_alias:
            conf = conf.replace(
                '<server_alias>', server_alias_https or server_alias
            ).replace(
                '<server_alias_opt>', ''
            )
        else:
            conf = conf.replace('<server_alias_opt>', '#')
    else:
        conf = apache_template

        if server_alias:
            conf = conf.replace(
                '<server_alias>', server_alias
            ).replace(
                '<server_alias_opt>', ''
            )
        else:
            conf = conf.replace('<server_alias_opt>', '#')

    if favicon:
        conf = conf.replace(
            '<favicon>', favicon
        ).replace(
            '<favicon_opt>', ''
        )
    else:
        conf = conf.replace('<favicon_opt>', '#')

    if version.LooseVersion(python_ver) >= version.LooseVersion('3.5'):
        conf = conf.replace(
            '<wsgi_daemon_process>', python35_wsgi_daemon_process_template
        )
    else:
        conf = conf.replace(
            '<wsgi_daemon_process>', python34_wsgi_daemon_process_template
        )

    conf = conf.replace(
        '<url>', url
    ).replace(
        '<email>', email
    ).replace(
        '<user>', user
    ).replace(
        '<git_dir>', git_dir
    ).replace(
        '<proj_dir>', proj_dir
    ).replace(
        '<wsgi_dir>', wsgi_dir
    ).replace(
        '<venv>', venv
    ).replace(
        '<python_ver>', python_ver
    ).replace(
        '<escaped_url>', url.replace('.', '\.')
    ).replace(
        '<url_dir>', url_dir
    )

    # print(conf)  # debug

    if create_file:
        if not filename:
            filename = url + '.conf'
        f = open(filename, 'w')
        f.write(conf)
        f.close()
        print('\nCreated file: ' + filename)

    return conf


if __name__ == '__main__':
    create_config()
