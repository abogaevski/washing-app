# washing-app
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
change settings file
    in wsgi.py
    in manage.py
    