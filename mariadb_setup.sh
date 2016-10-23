# Setup of mysql specific to Arch Linux which uses mariadb
mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
sudo mysqladmin -u root password
mysql -u root -p
# go in and make the db with 'create database DeckBuilderPro'
# update your config.py
sudo mysql -u root -p DeckBuilderPro < config/database-schema.sql
#starts it:
sudo /usr/bin/mysqld_safe --datadir='/var/lib/mysql'
