import MySQLdb
from passlib.hash import sha256_crypt
import qrcode
import os

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
    def insertPerson(self, username, password, firstname, lastname, phone, email, address, city):
        """

        This function returns Boolean: True or False

        :param username: string
        :param password: string
        :param firstname: string
        :param lastname: string
        :param phone: int
        :param email: string
        :param address: string
        :return: boolean
        """
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO user (username, password, firstname, lastname, phone, email, address, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (username, password, firstname, lastname, phone, email, address, city)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1

    #Insert image rgb code
    def insertImg(self, userid, img):
        """

        This function returns Boolean: True or False

        :param userid: int
        :param img: tuple
        :return: boolean
        """
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE user SET img = '{}' WHERE userid = '{}'".format(img, userid))
        self.connection.commit()
        return cursor.rowcount == 1

    #Check if username exist, username will be unique
    def checkUsername(self, username):
        """

        Check if username exist, username will be unique

        :param username: string
        :return: string
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = '{}'".format(username))
        if(cursor.rowcount >= 1):
            return False
        else:
            return True

    #Check persons username and encrypted password
    def checkPerson(self, username, password):
        """
        
        Check persons username and encrypted password

        :param username: string
        :param password: string
        :return: string
        """
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
        """

        Run this after checkPerson is completed to retrieve data

        :param username: string
        :return: string
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE username = '{}'".format(username))
            return cursor.fetchone()

    #Get available = 'True' cars
    def getAvailCar(self):
        """

        Get available = 'True' cars

        :return: boolean
        """

        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE available = 'True'")
            return cursor.fetchall()
    
    #Get individual car's info by int:carid
    def getCar(self, carid):
        """

        Get individual car's info by int:carid

        :param carid: int
        :return: int
        """

        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE carid = '{}'".format(carid))
            return cursor.fetchone()

    #Insert booking with follow intake parameters
    def insertBooking(self, userid, carid, cost, startDate, endDate, eventID):
        """

        Insert booking with follow intake parameters

        :param userid: int 
        :param carid: int
        :param cost: string
        :param startDate: date
        :param endDate: date
        :param eventID: int
        :return: int, string, date 
        """
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
        """

        Update car's availability with ( int:carid string:avail )

        :param carid: int
        :param avail: string
        :return: int , string
        """
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE car SET available = '{}' WHERE carid = '{}'".format(avail, carid))
        self.connection.commit()
        return cursor.rowcount == 1

    #Check car's availability with (int:carid) and return True or False
    def checkCarAvail(self, carid):
        """

        Check car's availability with (int:carid) and return True or False

        :param carid: int
        :return: boolean
        """
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
        """

        Get all booking filtered by userid

        :param userid: int
        :return: int 
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE userid = '{}' AND status = 'True'".format(userid))
            return cursor.fetchall()

    #Update booking status to "False"
    def cancelBooking(self, bookingid):
        """
        Update booking status to "False"
        :param bookingid: int
        :return: Boolean
        """
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE booking SET status = 'False' WHERE bookingid = '{}'".format(bookingid))
        self.connection.commit()
        return cursor.rowcount == 1
    
    #Get history of booking filtered by userid and status = "False", "False" means canceled
    def showHistory(self, userid):
        """

        Get history of booking filtered by userid and status = "False", "False" means canceled

        :param userid: int
        :return: Boolean 
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE userid = '{}' AND status != 'True'".format(userid))
            return cursor.fetchall()

    #Get single booking info by int:bookingid
    def getBooking(self, bookingid):
        """

        Get single booking info by int:bookingid

        :param bookingid: int
        :return: int
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE bookingid = '{}'".format(bookingid))
            return cursor.fetchone()

################## For server.py socket communication ##################

    # Get the image tuple numbers from AP and compare to database
    def checkFaceImage(self, img, carid, date):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE img = '{}'".format(img))
            if(cursor.rowcount >= 1):
                return self.checkImg_AP(cursor.fetchone()[1], carid, date)
            else:
                return [False, "img incorect or doesn't exist"]

    #Run this after checkPerson is completed to retrieve data
    def getPersonByID(self, userid):
        """
 
        Run this after checkPerson is completed to retrieve data
 
        :param username: string
        :return: string
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE userid = '{}'".format(userid))
            return cursor.fetchone()[1]
        
    def checkImg_AP(self, username, carid, date):
        """
 
        For server.py socket communication
 
        #1.Check username, password and generate userid for step 2
        
        #2.Check userid(from step 1), carid, date
 
        :param username: string
        :param password: string
        :param carid: int
        :param date: date
        :return: Boolean , string
        """
        if(self.checkUsername(username) == False):
            userid = self.getPerson(username)[0]
            booking = self.checkBooking_AP(userid, carid, date)
            if(booking):
                return [True, booking]
            else:
                return [False, "Error, You didn't book this car today"]
        else:
            return [False, "Username incorect or doesn't exist"]
    
    #1.Check username, password and generate userid for step 2
    #2.Check userid(from step 1), carid, date
    def checkLogin_AP(self, username, password, carid, date):
        """

        For server.py socket communication

        #1.Check username, password and generate userid for step 2
        
        #2.Check userid(from step 1), carid, date

        :param username: string
        :param password: string
        :param carid: int
        :param date: date
        :return: Boolean , string
        """
        if(self.checkUsername(username) == False):
            if(self.checkPerson(username, password)):
                userid = self.getPerson(username)[0]
                booking = self.checkBooking_AP(userid, carid, date)
                if(booking):
                    #If user booked this car during login date
                    #The return type is a tuple (bookingid, userid, carid, cost, startdate, enddate, totalcost, status, eventid)
                    #booking[0] will be the bookingid, we need this at client.py to do unlock/return
                    #Change to return booking[0] if you only want to return bookingid, otherwise do it at client side
                    return [True, booking]
                else:
                    return [False, "Error, You didn't book this car today"]
            else:
                return [False, "Error, Password is incorrect"]
        else:
            return [False, "Username incorect or doesn't exist"]

    #Helper function for checkLogin_AP
    def checkBooking_AP(self, userid, carid, date):
        """

        Helper function for checkLogin_AP

        :param userid: int
        :param carid: int
        :param date: date
        :return: int , date
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking where userid = '{}' AND carid = '{}' AND '{}' BETWEEN startdate AND enddate".format(userid, carid, date))
            return cursor.fetchone()

    #Unlock car by update booking status to Unlocked, returns True or False
    def unlock_AP(self, bookingid):
        """

        Unlock car by update booking status to Unlocked, returns True or False

        :param bookingid: int
        :return: Boolean
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE bookingid = '{}' AND status = 'True'".format(bookingid))
            if(cursor.rowcount == 1):
                cursor.execute("UPDATE booking SET status = 'Unlocked' WHERE bookingid = '{}'".format(bookingid))
            else:
                return False
        self.connection.commit()
        return cursor.rowcount == 1

    #Return car by update booking status to Returned, car's available to "True"
    #Need to update car location with Google Maps API
    def return_AP(self, bookingid):
        """

        #Return car by update booking status to Returned, car's available to "True"

        #Need to update car location with Google Maps API

        :param bookingid: int
        :return: Boolean
        """
        avail = "True"
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE bookingid = '{}' AND status = 'Unlocked'".format(bookingid))
            if(cursor.rowcount == 1):
                cursor.execute("UPDATE booking SET status = 'Returned' WHERE bookingid = '{}'".format(bookingid))
            else:
                return False
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

################## For A3 database functions ##################
    #This function returns Boolean: True or False
    def insertAdmin(self, username, password, firstname, lastname,phone,email,address):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO admin (username, password, firstname, lastname, phone, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (username, password, firstname, lastname, phone, email, address)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1

    #This function returns Boolean: True or False
    def insertManager(self, username, password, firstname, lastname,phone,email,address):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO manager (username, password, firstname, lastname, phone, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (username, password, firstname, lastname, phone, email, address)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1

    #This function returns Boolean: True or False
    def insertEngineer(self, username, password, firstname, lastname,phone,email,address):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO engineer (username, password, firstname, lastname, phone, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (username, password, firstname, lastname, phone, email, address)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1

    #Check admin encrypted username and encrypted password
    def checkAdmin(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM admin")
            results = cursor.fetchone()
            encName = results[1]
            userpass = results[2]
            if (sha256_crypt.verify(password, userpass) and sha256_crypt.verify(username, encName)):
                return True
            else:
                return False
    
    #Check admin encrypted username and encrypted password
    def checkManager(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM manager")
            results = cursor.fetchone()
            encName = results[1]
            userpass = results[2]
            if (sha256_crypt.verify(password, userpass) and sha256_crypt.verify(username, encName)):
                return True
            else:
                return False
    
    #Check admin encrypted username and encrypted password
    def checkEngineer(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM engineer")
            results = cursor.fetchone()
            encName = results[1]
            userpass = results[2]
            if (sha256_crypt.verify(password, userpass) and sha256_crypt.verify(username, encName)):
                return True
            else:
                return False

    #Check admin encrypted username and encrypted password
    def getAllBookings(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking")
            return cursor.fetchall()
    
    # Check admin encrypted username and encrypted password
    def getAllUsers(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user")
            return cursor.fetchall()

    # Get invididual user by userid
    def getUser(self, userid):
        """
 
        Get invididual user by userid
 
        :param username: string
        :return: string
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE userid = '{}'".format(userid))
            return cursor.fetchone()

    # Updating user with basic details and encrypte new password
    def updateUser(self, userid, username, password, firstname, lastname, phone, email, address, city):
        with self.connection.cursor() as cursor:
            if password == "":
                cursor.execute("UPDATE user SET firstname = '{}', lastname = '{}', phone = '{}', email = '{}', address = '{}', city = '{}' WHERE userid = '{}'".format(firstname, lastname, phone, email, address, city, userid))
            else:
                encpassword = sha256_crypt.hash(password)
                cursor.execute("UPDATE user SET password = '{}', firstname = '{}', lastname = '{}', phone = '{}', email = '{}', address = '{}', city = '{}' WHERE userid = '{}'".format(encpassword, firstname, lastname, phone, email, address, city, userid))
        self.connection.commit()
        return cursor.rowcount == 1
    
    # Get all cars no matter what the available status is
    def getAllCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car")
            return cursor.fetchall()

    # Updating car with new information
    def updateCar(self, carid, make, model, cartype, seats, color, location, cost, available, lat, lng):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE car SET make = '{}', model = '{}', type = '{}', seats = '{}', color = '{}', location = '{}', cost = '{}', available = '{}', lat = '{}', lng = '{}' WHERE carid = '{}'".format(make, model, cartype, seats, color, location, cost, available, lat, lng, carid))
        self.connection.commit()
        return cursor.rowcount == 1

    # delete car by CarID
    def deleteCar(self, carid):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM car WHERE carid = '{}'".format(carid))
        self.connection.commit()
        return cursor.rowcount == 1

    # delete user by UserID
    def deleteUser(self, userid):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM user WHERE userid = '{}'".format(userid))
        self.connection.commit()
        return cursor.rowcount == 1
    
    # Insert new car to database:car
    def addCar(self, make, model, cartype, seats, color, location, cost, available, lat, lng):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO car (make, model, type, seats, color, location, cost, available, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (make, model, cartype, seats, color, location, cost, available, lat, lng)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1
    
    # Report faulty car, setting its status to Faulty
    def reportCar(self, carid):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE car SET available = 'Faulty' WHERE carid = '{}'".format(carid))
        self.connection.commit()
        return cursor.rowcount == 1

    # Retrieve faulty car from database where available = "Faulty"
    def getFaultyCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE available = 'Faulty'")
            return cursor.fetchall()

    # Repair faulty car, setting its status to True
    def repairCar(self, carid):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE car SET available = 'True' WHERE carid = '{}'".format(carid))
        self.connection.commit()
        return cursor.rowcount == 1
    

# db = DatabaseUtils()
# print(db.checkAdmin("admin", "abc123"))