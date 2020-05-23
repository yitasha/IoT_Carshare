import unittest
import MySQLdb
from database import DatabaseUtils
from datetime import datetime

class TestDatabaseUtils(unittest.TestCase):
    HOST = "34.87.255.4"
    USER = "iotA2"
    PASSWORD = "Z4J96$\qg$:<ZxU6"
    DATABASE = "testcarshare"

    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(self):
        pass

    # code that is executed after all tests in one tes    
    # clean up logic for the test suite declared in the test modulet run
    @classmethod
    def tearDownClass(self):
        pass

    # code that is executed before each test
    def setUp(self):
        self.connection = MySQLdb.connect(TestDatabaseUtils.HOST, TestDatabaseUtils.USER,
            TestDatabaseUtils.PASSWORD, TestDatabaseUtils.DATABASE)
        with self.connection.cursor() as cursor:
            cursor.execute("drop table if exists booking")
            cursor.execute("""
                create table booking(
                    bookingid int NOT NULL auto_increment,
                    userid int NOT NULL,
                    carid  int NOT NULL,
                    cost int NOT NULL,
                    startdate DATE NOT NULL,
                    enddate DATE NOT NULL,
                    totalcost int NOT NULL,
                    status varchar(10) NOT NULL,
                    eventid varchar(30),
                    primary key (bookingid),
                    CONSTRAINT FK_userid FOREIGN KEY (userid) REFERENCES user(userid),
                    CONSTRAINT FK_carid FOREIGN KEY (carid) REFERENCES car(carid)
                )""")

            cursor.execute("""
                    INSERT INTO booking (userid, carid, cost, startdate, enddate, totalcost, status, eventid) VALUES (1, 1, 99, '2020-05-01', '2020-05-11', 990, 'False', 'Google Calendar EventID');
                    INSERT INTO booking (userid, carid, cost, startdate, enddate, totalcost, status, eventid) VALUES (2, 2, 459, '2020-05-05', '2020-05-10', 2295, 'True', 'Google Calendar EventID');
                    INSERT INTO booking (userid, carid, cost, startdate, enddate, totalcost, status, eventid) VALUES (3, 3, 249, '2020-05-10', '2020-05-15', 1245, 'True', 'Google Calendar EventID');
                """)
           
        self.connection.commit()

    # code that is executed after each test
    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countBooking(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM booking")
            return cursor.fetchone()[0]

    def countTrueBooking(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM booking WHERE status = 'True'")
            return cursor.fetchone()[0]
    
    def getBooking(self, bookingid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking WHERE bookingid = '{}'".format(bookingid))
            return cursor.fetchone()
    
    # Test insert booking
    def test_insertBooking(self):
        startDate =  datetime.strptime('2020-05-01', '%Y-%m-%d').date()
        endDate = datetime.strptime('2020-05-06', '%Y-%m-%d').date()
        counter = self.countBooking()
        with DatabaseUtils(self.connection) as db:
            self.assertTrue(db.insertBooking(4, 4, 199, startDate, endDate,'Google Calendar EventID'))
            self.assertEqual(counter + 1, self.countBooking())
    
    # Test get booking result from table filtered by status "True"
    def test_showBooking(self):
        with DatabaseUtils(self.connection) as db:
            # UserID 1 booked 1 car is False
            self.assertEqual(0, len(db.showBooking(1)))
            # UserID 10 booking doesn't exist
            self.assertEqual(0, len(db.showBooking(10)))

            # UserID 2 booked 1 car is True
            self.assertEqual(1, len(db.showBooking(2)))
            # UserID 3 booked 1 car is True
            self.assertEqual(1, len(db.showBooking(3)))
    
    # Test cancel booking by bookingID and count status:'True' 
    def test_cancelBooking(self):
        counter = self.countTrueBooking()
        with DatabaseUtils(self.connection) as db:
            self.assertTrue(db.cancelBooking(2))
            self.assertEqual(counter - 1, self.countTrueBooking())
            self.assertTrue(db.cancelBooking(3))
            self.assertEqual(counter - 2, self.countTrueBooking())
    
    # Test showing booking History, which is not "True"
    def test_showHistory(self):
        with DatabaseUtils(self.connection) as db:
            # UserID 1 have an canceled booking:'False'
            self.assertEqual(1, len(db.showHistory(1)))
            # UserID 2 have an active booking:'True'
            self.assertEqual(0, len(db.showHistory(2)))

            # Cancel UserID 2's booking and test again
            # Should be 1 canceled booking now instead of previous 0
            self.assertTrue(db.cancelBooking(2))
            self.assertEqual(1, len(db.showHistory(2)))

    # Test get Booking by bookingID and compare result
    def test_getBooking(self):
        with DatabaseUtils(self.connection) as db:
            self.assertEqual(self.getBooking(1), db.getBooking(1))

if __name__ == "__main__":
    unittest.main()