sudo mysql -u root -p

mysql -u root -p
password - intel#789

CREATE DATABASE intgbot;

CREATE USER 'botuser'@'localhost' IDENTIFIED BY 'intel#789';

# MYSQL 8.0 client:
# use mysql-connector-python instead of mysql-connector
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password' PASSWORD EXPIRE NEVER;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'intel#789';
ALTER USER 'botuser'@'localhost' IDENTIFIED BY 'password' PASSWORD EXPIRE NEVER;
ALTER USER 'botuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'intel#789';

revoke all privileges on intgbot.* from 'root'@'localhost' identified by 'intel#789';
grant all privileges on intgbot.* to 'botuser'@'localhost' identified by 'intel#789';
grant all privileges on intgbot.* to 'botuser'@'%' identified by 'intel#789';
flush privileges;

mysql -u botuser -p
password - intel#789
use intgbot;


create table clientprofile(client_id varchar(100), client_name varchar(100));
alter table clientprofile add primary key(client_id);
create table accountprofile(tenant_id varchar(100), client_id varchar(100), type varchar(50), model_accuracy varchar(20));
alter table accountprofile add primary key(tenant_id, client_id);
create table emailbotconfig(tenant_id varchar(100), incoming_server varchar(100), outgoing_server varchar(100), outgoing_port varchar(10), acc_user varchar(100), acc_psswd varchar(100), poll_interval varchar(10), api_endpoint varchar(100));
alter table emailbotconfig add primary key(tenant_id);
create table analysisdata(tenant_id varchar(100), acc_user varchar(100), message_keywords varchar(500), predicted_key varchar(100), prediction_accuracy varchar(20), request_ts varchar(100), creation_time varchar(100), batchprocess_time varchar(50));
alter table analysisdata add primary key(tenant_id, creation_time);

insert into clientprofile(select uuid(), 'Intelegencia');
select * from clientprofile;
insert into accountprofile(select uuid(), 'fa6f1a96-3a1b-11ea-8ccd-0028f8334ab4', 'emailbot', '0');
select * from accountprofile;
insert into emailbotconfig(tenant_id, incoming_server, outgoing_server, outgoing_port, acc_user, acc_psswd, poll_interval, api_endpoint) values('b20257c8-3a05-11ea-9c42-e4954081c65f', 'outlook.office365.com', 'smtp.office365.com', '587', 'assistant@intelegencia.com', 'Intel@02', '3600', 'http://127.0.0.1:8000/');
select * from emailbotconfig;
select * from analysisdata;
truncate table analysisdata;