Environment Scripts
===================

Requires Python 3

run:
```bash
python apache_config.py
```

follow instructions


Let's Encrypt
===
install:
`apt-get install letsencrypt`

stop web server (eg Apache):
`service apache2 stop`

run (replace <domain> / <subdomain>, can add multiple subdomains):
`letsencrypt certonly --standalone -d <domain> -d <subdomain>`

this will ask you to provide an email for recovery and to agree to a TOS

this should also output the files to `/etc/letsencrypt/live/<domain>/`

`apache_config.py` will ask for the full path to the files for the following settings:
`SSLCertificateFile` (fullchain.pem) / `SSLCertificateKeyFile` (privkey.pem)

once you've installed your site config test the SSL against https://www.ssllabs.com/ssltest/

run:
`letsencrypt renew`

this should output that no renewals were attempted. We need to run renew every so often to update our SSL certs

add the following to your sudo crontab (`sudo crontab -e`) (replace <domain>):
```
# Every Monday at 1:30 AM
30 1 * * 1 date >> /var/log/letsencrypt-renew/<domain>.log && /usr/sbin/service apache2 stop && /usr/bin/letsencrypt renew >> /var/log/letsencrypt-renew/<domain>.log 2>&1 && /usr/sbin/service apache2 start
```

make sure you create the log folder
`mkdir /var/log/letsencrypt-renew`

start web server (eg Apache):
`service apache2 start`
