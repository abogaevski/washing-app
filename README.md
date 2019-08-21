# washing-app

apt update
apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl mysql-server

if you create new database
    1. create database 
        create database <database_name> character set utf8;
    2. create user 
        CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
    3. grant privileges
        grant all privileges on <database_name>.* to '<username>'@'localhost';

    backup database
        mysqldump -uroot -p django_db > /home/odmen/dj_db.sql
    restore database
        mysql -uroot -p django_db < /home/ubuntu/dj_db.sql
cd /path/to/www
virtualenv env
git pull https://github.com/abogaevski/washing-app
source env/bin/activate
pip install -r requirements.txt
python3 manage.py runserver #test

nano /etc/systemd/system/gunicorn.socket
    
    [Unit]
    Description=gunicorn socket

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target

nano /etc/systemd/system/gunicorn.service
    
    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target

    [Service]
    User=sammy
    Group=www-data
    WorkingDirectory=/var/www/washing-app
    ExecStart=/var/www/washing-app/env/bin/gunicorn \
            --access-logfile - \
            --workers 3 \
            --bind unix:/run/gunicorn.sock \
            engine.wsgi:application

    [Install]
    WantedBy=multi-user.target

systemctl start gunicorn.socket
systemctl enable gunicorn.socket
systemctl enable gunicorn.socket
file /run/gunicorn.sock
journalctl -u gunicorn.socket
systemctl status gunicorn
curl --unix-socket /run/gunicorn.sock localhost
systemctl status gunicorn
nano /etc/nginx/sites-available/washing-app

    server {
        listen 80;
        server_name washing-app.by;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /var/www/washing-app/;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }

ln -s /etc/nginx/sites-available/washing-app /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx