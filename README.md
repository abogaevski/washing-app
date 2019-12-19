# Washing app

## Getting Started

### Installing

Install some prerequisites

    apt update
    apt install python3-pip python3-dev nginx curl mysql-server libmysqlclient-dev virtualenv mosquitto mosquitto-clients python3-venv gunicorn

### Configuring

##### Configuring MQTT

Run:
    
    sudo mosquitto_passwd -c /etc/mosquitto/passwd {%mqttuser%}
    nano /etc/mosquitto/conf.d/default.conf

And paste:

    allow_anonymous false
    password_file /etc/mosquitto/passwd

Enabling MQTT brocker:

    systemctl restart mosquitto

Note: change ip-adress of mqtt server in /your/www/washing-app/app/mqtt/subscriber.by and publisher.py files:
	client.connect("ipaddress", "port", timeaout_in_sec)


#### Configuring a database

If you have a database dump from another server you should to restore database from dump file.
For example:

    mysql -uroot -p <your_database_name> < /home/ubuntu/<your_database_dump_name>

If you create a new database:
    
    CREATE DATABASE <database_name> CHARACTER SET UTF8;
    CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
    GRANT ALL PRIVILEGES ON <database_name>.* TO '<username>'@'localhost';

Note: If need, change database name and user creds in /your/www/washing-app/engine/settings.py in DATABASES section


* [Create MySQL Database, Table & User From Command Line Guide](https://www.a2hosting.com/kb/developer-corner/mysql/managing-mysql-databases-and-users-from-the-command-line)
* [Creating and Selecting a Database](https://dev.mysql.com/doc/refman/8.0/en/creating-database.html)

Adding user for access from 1C server (only after you restore dump or migrate after new DB creation)

    CREATE USER '<1c_user>'@'%' IDENTIFIED BY '<password>';
    GRANT select on <database_name>.app_card to '<1c_user>'@'%';
    GRANT select on <database_name>.app_contractor to '<1c_user>'@'%';
    GRANT select on <database_name>.app_partner to '<1c_user>'@'%';
    GRANT select on <database_name>.app_payment to '<1c_user>'@'%';
    GRANT select on <database_name>.app_post to '<1c_user>'@'%';
    GRANT select on <database_name>.app_station to '<1c_user>'@'%';
    GRANT select on <database_name>.app_transaction to '<1c_user>'@'%';
    GRANT select on <database_name>.app_usertransaction to '<1c_user>'@'%';

Database cleaning

    DROP DATABASE <database_name>;
    #create new database as shown above
    #DROP action do not affect on users


#### Configuring a Django webapp

Virtual environment:

    cd <your/www/>;
    git clone https://github.com/abogaevski/washing-app
    cd <your/www/washing-app>;
    chown -R www-data:www-data ./
    chmod -R 755 ./
    python3 -m venv env

Configure a django webapp:

    source env/bin/activate

    pip3 install -r requirements.txt

    mkdir logs
    touch logs/django.log



Test your app:

    python3 manage.py runserver

If your database is new, run:

    python3 manage.py migrate

And test again.
If OK, than create site admin

    python3 manage.py createsuperuser




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
            --workers 1 \
            --bind unix:/run/gunicorn.sock \
            engine.wsgi:application

    [Install]
    WantedBy=multi-user.target

##### Enabling new systemd service

Run:

    systemctl start gunicorn.socket
    systemctl start gunicorn.service
    systemctl enable gunicorn.socket
    systemctl enable gunicorn.service
    
    # Check if file is exist
    file /run/gunicorn.sock

    # Check last service logs
    journalctl -u gunicorn.socket
    systemctl start gunicorn
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

Make symlink:

    ln -s /etc/nginx/sites-available/washing-app /etc/nginx/sites-enabled/washing-app
    rm /etc/nginx/sites-available/default
    rm /etc/nginx/sites-enabled/default
    service nginx restart


Final action:

    cd /your/www/washing-app
    source env/bin/activate
    python3 manage.py collectstatic


## What we have now

- Database: **django_db**
- WWW path: **/var/www/washing-app/**
- Nginx logs: **/var/log/nginx**
- Gunicorn logs: **/var/log/gunicorn**
- Django logs: **var/www/washing-app/logs/** 
> Mqtt logs are the same path as specified above

### Changes

Just pull the changes and restart gunicorn server

    cd /var/www/washing-app/
    git pull
    service gunicorn restart

### Some info

#### Django
- [Django documentation](https://docs.djangoproject.com/en/2.2/)
- [Paho MQTT](https://www.eclipse.org/paho/clients/python/docs/)

#### Nginx
- [Nginx docs](https://nginx.org/ru/docs/)
- [Nginx ngx_http_proxy_module](http://nginx.org/ru/docs/http/ngx_http_proxy_module.html)

#### Gunicorn
- [Gunicorn configuration](http://docs.gunicorn.org/en/latest/configure.html)


## Celery configuration

    sudo apt-get install redis-server
    sudo useradd celery -d /home/celery -b /bin/bash
    sudo nano /etc/tmpfiles.d/celery.conf

        d /var/run/celery 0755 celery celery -
        d /var/log/celery 0755 celery celery -
    
    sudo mkdir /var/log/celery
    sudo chown -R celery:celery /var/log/celery
    sudo chmod -R 755 /var/log/celery

    sudo mkdir /var/run/celery
    sudo chown -R celery:celery /var/run/celery
    sudo chmod -R 755 /var/run/celery

    sudo nano /etc/conf.d/celery

        CELERYD_NODES="washing-app"
        CELERY_BIN="/var/www/washing-app/env/bin/celery"
        CELERY_APP="engine"
        CELERYD_MULTI="multi"
        CELERYD_OPTS="--time-limit=300 --concurrency=8"
        CELERYD_PID_FILE="/var/run/celery/%n.pid"
        CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
        CELERYD_LOG_LEVEL="INFO"
        CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
        CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"


    sudo nano /etc/systemd/system/celery.service
        
        [Unit]
        Description=Celery Service
        After=network.target

        [Service]
        Type=forking
        User=celery
        Group=celery
        EnvironmentFile=/etc/conf.d/celery
        WorkingDirectory=/var/www/washing-app/

        ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
        -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
        --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
        ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
        --pidfile=${CELERYD_PID_FILE}'
        ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
        -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
        --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

        [Install]
        WantedBy=multi-user.target

    sudo nano /etc/systemd/system/celerybeat.service

        [Unit]
        Description=Celery Beat Service
        After=network.target

        [Service]
        Type=simple
        User=celery
        Group=celery
        EnvironmentFile=/etc/conf.d/celery
        WorkingDirectory=/var/www/washing-app/
        ExecStart=/bin/sh -c '${CELERY_BIN} beat  \
        -A ${CELERY_APP} --pidfile=${CELERYBEAT_PID_FILE} \
        --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'

        [Install]
        WantedBy=multi-user.target

    sudo systemctl daemon-reload
    sudo systemctl enable celery
    sudo systemctl enable celerybeat

    service celerybeat start
    service celery start
    



