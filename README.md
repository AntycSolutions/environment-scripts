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
`sudo apt install letsencrypt`

stop web server (eg Apache):
`sudo service apache2 stop`

run (replace \<domain> / \<subdomain>, can add multiple subdomains):
`sudo letsencrypt certonly --standalone -d <domain> -d <subdomain>`

this will ask you to provide an email for recovery and to agree to a TOS

this should also output the files to `/etc/letsencrypt/live/<domain>/`

`apache_config.py` will ask for the full path to the files for the following settings:
`SSLCertificateFile` (fullchain.pem) / `SSLCertificateKeyFile` (privkey.pem)

once you've installed your site config test the SSL against https://www.ssllabs.com/ssltest/

run:
`sudo letsencrypt renew`

this should output that no renewals were attempted. We need to run renew every so often to update our SSL certs

add the following to your sudo crontab (`sudo crontab -e`):
```
# Every Monday at 1:30 AM
30 1 * * 1 /path/to/letsencrypt_renew.sh >> /var/log/letsencrypt-renew/renew.log 2>&1
```

make sure you create the log folder
`sudo mkdir -p /var/log/letsencrypt-renew`

start web server (eg Apache):
`sudo service apache2 start`
