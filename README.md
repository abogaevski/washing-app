# washing-app

1. apt update
2. apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl mysql-server

2.1. if you create new database
   
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

3. cd /path/to/www;
4. virtualenv env
5. git pull https://github.com/abogaevski/washing-app
6. source env/bin/activate
7. pip install -r requirements.txt
8. python3 manage.py runserver #test

9. nano /etc/systemd/system/gunicorn.socket
    
        [Unit]
        Description=gunicorn socket

        [Socket]
        ListenStream=/run/gunicorn.sock

        [Install]
        WantedBy=sockets.target

10. nano /etc/systemd/system/gunicorn.service
    
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

11. systemctl start gunicorn.socket
12. systemctl enable gunicorn.socket
13. systemctl enable gunicorn.socket
14. file /run/gunicorn.sock
15. journalctl -u gunicorn.socket
16. systemctl status gunicorn
17. curl --unix-socket /run/gunicorn.sock localhost
18. systemctl status gunicorn
19. nano /etc/nginx/sites-available/washing-app

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