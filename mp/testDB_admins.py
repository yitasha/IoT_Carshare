import unittest
import MySQLdb
from database import DatabaseUtils
from passlib.hash import sha256_crypt

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
            cursor.execute("drop table if exists admin")
            cursor.execute("drop table if exists manager")
            cursor.execute("drop table if exists engineer")
            cursor.execute("""
                create table admin(
                    adminid int NOT NULL auto_increment,
                    username text NOT NULL,
                    password text NOT NULL,
                    firstname  varchar(20) NOT NULL,
                    lastname varchar (20) NOT NULL,
                    phone varchar(15) NOT NULL,
                    email varchar (40) NOT NULL,
                    address varchar (40) NOT NULL,
                    img text,
                    primary key (adminid)
                )""")
            cursor.execute("""
                create table manager(
                    managerid int NOT NULL auto_increment,
                    username text NOT NULL,
                    password text NOT NULL,
                    firstname  varchar(20) NOT NULL,
                    lastname varchar (20) NOT NULL,
                    phone varchar(15) NOT NULL,
                    email varchar (40) NOT NULL,
                    address varchar (40) NOT NULL,
                    img text,
                    primary key (managerid)
                )""")
            cursor.execute("""
                create table engineer(
                    engineid int NOT NULL auto_increment,
                    username text NOT NULL,
                    password text NOT NULL,
                    firstname  varchar(20) NOT NULL,
                    lastname varchar (20) NOT NULL,
                    phone varchar(15) NOT NULL,
                    email varchar (40) NOT NULL,
                    address varchar (40) NOT NULL,
                    img text,
                    primary key (engineid)
                )""")
        self.connection.commit()

    # code that is executed after each test
    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def countAdmin(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM admin")
            return cursor.fetchone()[0]

    def countManager(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM manager")
            return cursor.fetchone()[0]

    def countEngineer(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM engineer")
            return cursor.fetchone()[0]

    # Insert admin and check for count rows
    def test_insertAdmin(self):
        with DatabaseUtils(self.connection) as db:
            count = self.countAdmin()
            username = sha256_crypt.hash("TestAdmin")
            password = sha256_crypt.hash("TestPassword")
            # Perform test
            self.assertTrue(db.insertAdmin(username, password, "TestFirstName", "TestLastName", "TestPhone", "TestEmail@gmail.com","TestAddress"))
            self.assertTrue((count + 1) == self.countAdmin())
    
    # Insert manager and check for count rows
    def test_insertManager(self):
        with DatabaseUtils(self.connection) as db:
            count = self.countManager()
            username = sha256_crypt.hash("TestManager")
            password = sha256_crypt.hash("TestPassword")
            # Perform test
            self.assertTrue(db.insertManager(username, password, "TestFirstName", "TestLastName", "TestPhone", "TestEmail@gmail.com","TestAddress"))
            self.assertTrue((count + 1) == self.countManager())
    
    # Insert engineer and check for count rows
    def test_insertEngineer(self):
        with DatabaseUtils(self.connection) as db:
            count = self.countEngineer()
            username = sha256_crypt.hash("TestEngineer")
            password = sha256_crypt.hash("TestPassword")
            # Perform test
            self.assertTrue(db.insertEngineer(username, password, "TestFirstName", "TestLastName", "TestPhone", "TestEmail@gmail.com","TestAddress"))
            self.assertTrue((count + 1) == self.countEngineer())

if __name__ == "__main__":
    unittest.main()
