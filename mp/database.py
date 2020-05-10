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
    
    #Get individual car's info by int:carid
    def getCar(self, carid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE carid = '{}'".format(carid))
            return cursor.fetchone()

    #Insert booking with follow intake parameters
    def insertBooking(self, userid, carid, cost, startDate, endDate, eventID):
        #calculate totalcost
        days = endDate - startDate
        totalcost = days.days * cost
        #Status for this booking event - Default: active
        status = "True" 
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO booking (userid, carid, cost, startdate, enddate, totalcost, status, eventid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (userid, carid, cost, startDate, endDate, int(totalcost), status, eventID)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1
    
    #Update car's availability with ( int:carid string:avail )
    def updateCarAvail(self, carid, avail):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE car SET available = '{}' WHERE carid = '{}'".format(avail, carid))
        self.connection.commit()
        return cursor.rowcount == 1

    #Check car's availability with (int:carid) and return True or False
    def checkCarAvail(self, carid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE carid = '{}'".format(carid))
            results = cursor.fetchone()
            availability = results[8]
            if(availability == "True"):
                return True
            else:
                return False
    
    #Get all booking filtered by userid
    def showBooking(self, userid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE userid = '{}' AND status = 'True'".format(userid))
            return cursor.fetchall()

    #Update booking status to "False"
    def cancelBooking(self, bookingid):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE booking SET status = 'False' WHERE bookingid = '{}'".format(bookingid))
        self.connection.commit()
        return cursor.rowcount == 1
    
    #Get history of booking filtered by userid and status = "False", "False" means canceled
    def showHistory(self, userid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE userid = '{}' AND status = 'False'".format(userid))
            return cursor.fetchall()

    #Get single booking info by int:bookingid
    def getBooking(self, bookingid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE bookingid = '{}'".format(bookingid))
            return cursor.fetchone()

################## For server.py socket communication ##################
    #1.Check username, password and generate userid for step 2
    #2.Check userid(from step 1), carid, date
    def checkLogin_AP(self, username, password, carid, date):
        if(self.checkUsername(username) == False):
            if(self.checkPerson(username, password)):
                userid = self.getPerson(username)[0]
                booking = self.checkBooking_AP(userid, carid, date)
                if(booking):
                    #If user booked this car at during login date
                    #The return type is a tuple (bookingid, userid, carid, cost, startdate, enddate, totalcost, status, eventid)
                    #booking[0] will be the bookingid, we need this at client.py to unlock/return
                    return booking
                else:
                    return "Error, You didn't book this car today"
            else:
                return "Error, Password is incorrect"
        else:
            return "Username incorect or doesn't exist"
    
    #Helper function for checkLogin_AP
    def checkBooking_AP(self, userid, carid, date):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking where userid = '{}' AND carid = '{}' AND '{}' BETWEEN startdate AND enddate".format(userid, carid, date))
            return cursor.fetchone()

    #Unlock car by update booking status to Unlocked, returns True or False
    def unlock_AP(self, bookingid):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE booking SET status = 'Unlocked' WHERE bookingid = '{}'".format(bookingid))
        self.connection.commit()
        return cursor.rowcount == 1

    #Return car by update booking status to Returned, car's available to "True"
    #Need to update car location with Google Maps API
    def return_AP(self, bookingid):
        avail = "True"
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE booking SET status = 'Returned' WHERE bookingid = '{}'".format(bookingid))
        self.connection.commit()
        #If Booking status is updated on success
        if(cursor.rowcount == 1):
            #Get booking data
            booking = self.getBooking(bookingid)
            #Set the carid available to True from this booking, carid is indexed at [2]
            if(self.updateCarAvail(booking[2], avail)):
                return True
            else:
                return False
        else:
            return False
