# Washing app

## Getting Started

### Installing

Install some prerequisites

    apt update
    apt install python3-pip python3-dev nginx curl mysql-server virtualenv mosquitto mosquitto-clients

### Configuring

#### Configuring a database

If you have a database dump from another server you should to restore database from dump file.
For example:

    mysql -uroot -p <your_database_name> < /home/ubuntu/<your_database_dump_name>

If you create a new database:
    
    CREATE DATABASE <database_name> CHARACTER SET UTF8;
    CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
    GRANT ALL PRIVILEGES ON <database_name>.* TO '<username>'@'localhost';

* [Create MySQL Database, Table & User From Command Line Guide](https://www.a2hosting.com/kb/developer-corner/mysql/managing-mysql-databases-and-users-from-the-command-line)
* [Creating and Selecting a Database](https://dev.mysql.com/doc/refman/8.0/en/creating-database.html)

Adding user for access from 1C server

    CREATE USER '<1c_user>'@'%' IDENTIFIED BY 'password';
    GRANT select on django_db.app_card to '<1c_user>'@'%';
    GRANT select on django_db.app_contractor to '<1c_user>'@'%';
    GRANT select on django_db.app_partner to '<1c_user>'@'%';
    GRANT select on django_db.app_payment to '<1c_user>'@'%';
    GRANT select on django_db.app_post to '<1c_user>'@'%';
    GRANT select on django_db.app_station to '<1c_user>'@'%';
    GRANT select on django_db.app_transaction to '<1c_user>'@'%';
    GRANT select on django_db.app_usertransaction to '<1c_user>'@'%';

#### Configuring a Django webapp

Virtual environment:

    cd <your/www/path/>;
    virtualenv env

Configure a django webapp:

    git pull https://github.com/abogaevski/washing-app
    source env/bin/activate
    pip install -r requirements.txt

Test your app:

    python3 manage.py runserver

If your database is new, run:

    python3 manage.py migrate

And test again.

[Установка Django](https://tutorial.djangogirls.org/ru/django_installation/)

#### Configuring python container Gunicorn

##### Configuring systemd socket.

Run:

    nano /etc/systemd/system/gunicorn.socket

And paste: 

    [Unit]
    Description=gunicorn socket

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target

##### Configuring systemd service.
Run:

    nano /etc/systemd/system/gunicorn.service

Paste:

    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/var/www/washing-app
    ExecStart=/var/www/washing-app/env/bin/gunicorn \
            --error-logfile /var/log/gunicorn/error.log \
            --access-logfile /var/log/gunicorn/access.log \
            --workers 3 \
            --bind unix:/run/gunicorn.sock \
            engine.wsgi:application

    [Install]
    WantedBy=multi-user.target

##### Enabling new systemd service

Run:

    systemctl start gunicorn.socket
    systemctl enable gunicorn.socket
    systemctl enable gunicorn.socket
    
    # Check if file is exist
    file /run/gunicorn.sock

    # Check last service logs
    journalctl -u gunicorn.socket
    systemctl status gunicorn

    # Check if you get a response
    curl --unix-socket /run/gunicorn.sock localhost

    # Check your service status
    systemctl status gunicorn

##### Configuring Nginx

Run:
    
    nano /etc/nginx/sites-available/washing-app

And paste:

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


##### Configuring MQTT

Run:
    
    sudo mosquitto_passwd -c /etc/mosquitto/passwd {%mqttuser%}
    nano /etc/mosquitto/conf.d/default.conf

And paste:

    allow_anonymous false
    password_file /etc/mosquitto/passwd

Enabling MQTT brocker:

    systemctl restart mosquitto

## What we have now

- Database: **django_db**
- WWW path: **/var/www/washing-app/**
- Nginx logs: **/var/log/nginx**
- Gunicorn logs: **/var/log/gunicorn**
- Django logs: **var/www/washing-app/logs/** 
> Mqtt logs are the same path as specified above

### Some info

#### Django
- [Django documentation](https://docs.djangoproject.com/en/2.2/)
- [Paho MQTT](https://www.eclipse.org/paho/clients/python/docs/)

#### Nginx
- [Nginx docs](https://nginx.org/ru/docs/)
- [Nginx ngx_http_proxy_module](http://nginx.org/ru/docs/http/ngx_http_proxy_module.html)

#### Gunicorn
- [Gunicorn configuration](http://docs.gunicorn.org/en/latest/configure.html)
