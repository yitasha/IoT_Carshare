import unittest
import MySQLdb
from database import DatabaseUtils

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
            cursor.execute("drop table if exists car")
            cursor.execute("""
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
                )""")
            
            cursor.execute("""
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
    
    def countCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM car")
            return cursor.fetchone()[0]
    
    def getAvailCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE available = 'True'")
            return cursor.fetchall()
    
    def countAvailCar(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM car WHERE available = 'True'")
            return cursor.fetchone()[0]

    def getCar(self, carid):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM car WHERE carid = '{}'".format(carid))
            return cursor.fetchone()

    # Compare the available cars row count
    def test_countAvailCar(self):
        with DatabaseUtils(self.connection) as db:
            self.assertEqual(self.countAvailCar(), len(db.getAvailCar()))
        
    # Compare the available cars data
    def test_getAvailCar(self):
        with DatabaseUtils(self.connection) as db:
            self.assertEqual(self.getAvailCar(), db.getAvailCar())

    # Compare the available cars data with function and manual raw data
    def test_getCar(self):
        with DatabaseUtils(self.connection) as db:
            self.assertEqual(self.getCar(1), db.getCar(1))
            self.assertEqual(self.getCar(2), db.getCar(2))
            rawData20 = (20, "Ferrari", "F1", "SUV", "5", "Red", "South Yarra", 1299, "False")
            rawData10 = (10, "Volvo", "XC60", "SUV", "5", "White", "Carlton", 199, "True")
            self.assertEqual(rawData10, db.getCar(10))
            self.assertEqual(rawData20, db.getCar(20))
    
    # Test updating car availability
    def test_updateCarAvail(self):
        status_F = "False"
        status_T = "True"
        car1 = 1
        car2 = 2
        currentAvail = self.countAvailCar()
        with DatabaseUtils(self.connection) as db:
            # Set status to False and compare with counter
            self.assertTrue(db.updateCarAvail(car1, status_F))
            self.assertEqual(currentAvail - 1, self.countAvailCar())
            self.assertTrue(db.updateCarAvail(car2, status_F))
            self.assertEqual(currentAvail - 2, self.countAvailCar())
            # Set status to True and compare backward with counter
            self.assertTrue(db.updateCarAvail(car2, status_T))
            self.assertEqual(currentAvail - 1, self.countAvailCar())
            self.assertTrue(db.updateCarAvail(car1, status_T))
            self.assertEqual(currentAvail, self.countAvailCar())
    
    # Test car's availability
    def test_checkCarAvail(self):
        carTrue1 = 1
        carTrue2 = 2
        carFalse19 = 19
        carFalse20 = 20
        with DatabaseUtils(self.connection) as db:
            self.assertTrue(db.checkCarAvail(carTrue1))
            self.assertTrue(db.checkCarAvail(carTrue2))
            self.assertFalse(db.checkCarAvail(carFalse19))
            self.assertFalse(db.checkCarAvail(carFalse20))

if __name__ == "__main__":
    unittest.main()

