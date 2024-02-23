CREATE USER 'test'@'10.2.1.17' IDENTIFIED WITH mysql_native_password BY 'test';
GRANT ALL PRIVILEGES ON *.* TO 'test'@'10.2.1.17';
FLUSH PRIVILEGES;

