drop database if exists carshare;
create database carshare;
use carshare;

create table user(
userid int NOT NULL auto_increment,
username varchar(20) NOT NULL,
password varchar (30) NOT NULL,
firstname  varchar(20) NOT NULL,
lastname varchar (20) NOT NULL,
phone varchar(15) NOT NULL,
email varchar (40) NOT NULL,
address varchar (40) NOT NULL,
primary key (userid)
);

create table car(
carid int NOT NULL auto_increment,
make varchar(30) NOT NULL,
model varchar (20) NOT NULL,
type  varchar(20) NOT NULL,
seats varchar(20) NOT NULL,
color varchar (20) NOT NULL,
location varchar (30) NOT NULL,
cost int NOT NULL,
available varchar(10) NOT NULL,
primary key (carid)
);

create table booking(
bookingid int NOT NULL auto_increment,
userid int NOT NULL,
carid  int NOT NULL,
cost int NOT NULL,
startdate DATE NOT NULL,
enddate DATE NOT NULL,
totalcost int NOT NULL,
primary key (bookingid),
CONSTRAINT FK_userid FOREIGN KEY (userid) REFERENCES user(userid),
CONSTRAINT FK_carid FOREIGN KEY (carid) REFERENCES car(carid)
);
