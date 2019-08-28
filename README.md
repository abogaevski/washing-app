# Washing app

## Getting Started

### Installing

Install some prerequisites

    apt update
    apt install python3-pip python3-dev nginx curl mysql-server virtualenv

### Configuring

#### Configuring a database

If you have a database dump from another server you should to restore database from dump file.
For example:

    mysql -uroot -p <your_database_name> < /home/ubuntu/<your_database_dump_name>

If you create a new database:
    
    1. CREATE DATABASE <database_name> CHARACTER SET UTF8;
    2. CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
    3. GRANT ALL PRIVILEGES ON <database_name>.* TO '<username>'@'localhost';

* [Create MySQL Database, Table & User From Command Line Guide](https://www.a2hosting.com/kb/developer-corner/mysql/managing-mysql-databases-and-users-from-the-command-line)
* [Creating and Selecting a Database](https://dev.mysql.com/doc/refman/8.0/en/creating-database.html)


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

Enabling new site:

    ln -s /etc/nginx/sites-available/washing-app /etc/nginx/sites-enabled
    nginx -t
    systemctl restart nginx