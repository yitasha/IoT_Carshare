import MySQLdb
from passlib.hash import sha256_crypt

class DatabaseUtils:
    HOST = "35.189.49.76"
    USER = "root"
    PASSWORD = "root"
    DATABASE = "carshare"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(DatabaseUtils.HOST, DatabaseUtils.USER, DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createPersonTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                create table if not exists Person (
                    PersonID int not null auto_increment,
                    Name text not null,
                    constraint PK_Person primary key (PersonID)
                )""")
        self.connection.commit()
    
    #This function returns Boolean: True or False
    def insertPerson(self, username, password, firstname, lastname,phone,email,address):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO user (username, password, firstname, lastname, phone, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (username, password, firstname, lastname, phone, email, address)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1

    #Check persons username and encrypted password
    def checkPerson(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user where username = '{}'".format(username))
            results = cursor.fetchone()
            userpass = results[2]
            if (sha256_crypt.verify(password, userpass)):
                return True
            else:
                return False

    #Run this after checkPerson is completed to retrieve data
    def getPerson(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user where username = '{}'".format(username))
            return cursor.fetchone()

    #Get available = 'True' cars
    def getAvailCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car where available = 'True'")
            return cursor.fetchall()

    def insertBooking(self, userid, carid, cost, startDate, endDate):
        #calculate totalcost
        days = endDate - startDate
        totalcost = days.days * cost
        #Status for this booking event - Default: active
        status = "True" 
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO booking (userid, carid, cost, startdate, enddate, totalcost, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (userid, carid, cost, startDate, endDate, int(totalcost), status)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1
    
    def updateCarAvail(self, carid, avail):
        condition = avail
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE car SET available = '{}' where carid = '{}'".format(condition, carid))
        self.connection.commit()
        return cursor.rowcount == 1

    def checkCarAvail(self, carid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car where carid = '{}'".format(carid))
            results = cursor.fetchone()
            availability = results[8]
            if(availability == "True"):
                return True
            else:
                return False
        
        

################## Testing ##################
    def getPeople(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from user")
            return cursor.fetchall()

    def deletePerson(self, personID):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from Person where PersonID = %s", (personID))
        self.connection.commit()
