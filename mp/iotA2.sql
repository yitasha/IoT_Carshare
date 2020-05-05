drop database if exists carshare;
create database carshare;
use carshare;

create table user(
userid int NOT NULL auto_increment,
username text NOT NULL,
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

/* Dummy Data for tables */
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Toyota", "Camry", "Sedan", "5", "Red", "Melbourne", 99, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("BMW", "i8", "Coupe", "2", "Blue", "Sydney", 459, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("BMW", "i320", "Sedan", "5", "White", "Geelong", 249, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Mazda", "CX-5", "SUV", "5", "Red", "RMIT", 199, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Mitsubishi", "Lancer", "Sedan", "5", "Black", "Rowville", 129, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Nissan", "Skyline", "Coupe", "4", "Red", "Ringwood", 199, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Porsche", "911", "Coupe", "2", "Red", "Glen Waverly", 999, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("VW", "Golf", "Hatchback", "4", "Black", "Kew", 99, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Porsche", "Cayenne", "SUV", "5", "Yellow", "Melbourne", 799, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Volvo", "XC60", "SUV", "5", "White", "Carlton", 199, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Porsche", "Panamera", "Sedan", "4", "Black", "Melbourne", 799, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("AUDI", "A4", "Sedan", "5", "Green", "Melbourne", 399, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Honda", "Civic", "Sedan", "5", "Black", "Melbourne", 99, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Toyota", "Corolla", "Hatch", "5", "Navy", "Point Cook", 69, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Hyundai", "i30", "Hatch", "5", "White", "Melbourne", 69, "True");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Hyundai", "i20", "Hatch", "5", "Black", "Hawthorn", 69, "False");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("AUDI", "i20", "Hatch", "5", "Black", "Hawthorn", 69, "False");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Nissan", "Fairlady-Z", "Coupe", "2", "Black", "Hawthorn", 69, "False");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Ferrari", "F8", "Coupe", "2", "Black", "Hawthorn", 999, "False");
INSERT INTO car (make, model, type, seats, color, location, cost, available) VALUES ("Ferrari", "F1", "SUV", "5", "Red", "South Yarra", 1299, "False");



