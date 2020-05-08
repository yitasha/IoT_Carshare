import MySQLdb
from passlib.hash import sha256_crypt

class DatabaseUtils:
    HOST = "35.189.49.76"
    USER = "iotA2"
    PASSWORD = "Z4J96$\qg$:<ZxU6"
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
    
    #This function returns Boolean: True or False
    def insertPerson(self, username, password, firstname, lastname,phone,email,address):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO user (username, password, firstname, lastname, phone, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (username, password, firstname, lastname, phone, email, address)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1

    #Check if username exist, username will be unique
    def checkUsername(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = '{}'".format(username))
        self.connection.commit()
        if(cursor.rowcount >= 1):
            return False
        else:
            return True

    #Check persons username and encrypted password
    def checkPerson(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = '{}'".format(username))
            results = cursor.fetchone()
            userpass = results[2]
            if (sha256_crypt.verify(password, userpass)):
                return True
            else:
                return False

    #Run this after checkPerson is completed to retrieve data
    def getPerson(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = '{}'".format(username))
            return cursor.fetchone()

    #Get available = 'True' cars
    def getAvailCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE available = 'True'")
            return cursor.fetchall()
    
    def getCar(self, carid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE carid = '{}'".format(carid))
            return cursor.fetchone()

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
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE car SET available = '{}' WHERE carid = '{}'".format(avail, carid))
        self.connection.commit()
        return cursor.rowcount == 1

    def checkCarAvail(self, carid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE carid = '{}'".format(carid))
            results = cursor.fetchone()
            availability = results[8]
            if(availability == "True"):
                return True
            else:
                return False
        
    def showBooking(self, userid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE userid = '{}' AND status = 'True'".format(userid))
            return cursor.fetchall()

    def cancelBooking(self, bookingid):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE booking SET status = 'False' WHERE bookingid = '{}'".format(bookingid))
        self.connection.commit()
        return cursor.rowcount == 1
    
    def showHistory(self, userid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE userid = '{}' AND status = 'False'".format(userid))
            return cursor.fetchall()

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
