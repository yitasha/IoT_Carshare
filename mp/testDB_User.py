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
            cursor.execute("drop table if exists user")
            cursor.execute("""
                create table if not exists user (
                    userid int NOT NULL auto_increment,
                    username text NOT NULL,
                    password text NOT NULL,
                    firstname  varchar(20) NOT NULL,
                    lastname varchar (20) NOT NULL,
                    phone varchar(15) NOT NULL,
                    email varchar (40) NOT NULL,
                    address varchar (40) NOT NULL,
                    primary key (userid)
                )""")
            
            password = sha256_crypt.hash("TestPassword")
            cursor.execute("INSERT INTO user (username, password, firstname, lastname, phone, email, address) VALUES ('TestUser1', '{}', 'TestFirstName', 'TestLastName', 'TestPhone', 'TestEmail', 'TestAddress')".format(password))
            cursor.execute("INSERT INTO user (username, password, firstname, lastname, phone, email, address) VALUES ('TestUser2', '{}', 'TestFirstName', 'TestLastName', 'TestPhone', 'TestEmail', 'TestAddress')".format(password))
            cursor.execute("INSERT INTO user (username, password, firstname, lastname, phone, email, address) VALUES ('TestUser3', '{}', 'TestFirstName', 'TestLastName', 'TestPhone', 'TestEmail', 'TestAddress')".format(password))
        self.connection.commit()

    # code that is executed after each test
    def tearDown(self):
        try:
            self.connection.close()
        except:
            pass
        finally:
            self.connection = None
    
    def countPeople(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM user")
            return cursor.fetchone()[0]

    def test_insertPerson(self):
        with DatabaseUtils(self.connection) as db:
            count = self.countPeople()
            password = sha256_crypt.hash("TestPassword")

            self.assertTrue(db.insertPerson("TestUser4", password,"TestFirstName","TestLastName","TestPhone","TestEmail","TestAddress"))
            self.assertTrue((count + 1) == self.countPeople())
            self.assertTrue(db.insertPerson("TestUser5", password,"TestFirstName","TestLastName","TestPhone","TestEmail","TestAddress"))
            self.assertTrue((count + 2) == self.countPeople())
    
    # This checks if a username is available
    def test_checkUsername(self):
        with DatabaseUtils(self.connection) as db:
            self.assertFalse(db.checkUsername("TestUser1"))
            self.assertFalse(db.checkUsername("TestUser2"))
            self.assertFalse(db.checkUsername("TestUser3"))
            self.assertTrue(db.checkUsername("FakeUser"))
            self.assertTrue(db.checkUsername("FakeUserAccount"))
            self.assertTrue(db.checkUsername("FakeUserRoot"))
    
    # Checks username & encrypted password
    def test_checkPerson(self):
        with DatabaseUtils(self.connection) as db:
            self.assertTrue(db.checkPerson("TestUser1", "TestPassword"))
            self.assertTrue(db.checkPerson("TestUser2", "TestPassword"))
            self.assertTrue(db.checkPerson("TestUser3", "TestPassword"))
            self.assertFalse(db.checkPerson("TestUser1", "WrongPassword1"))
            self.assertFalse(db.checkPerson("TestUser2", "WrongPassword2"))
            self.assertFalse(db.checkPerson("TestUser3", "WrongPassword3"))
    
    # Checks user
    def test_getPerson(self):
        with DatabaseUtils(self.connection) as db:
            self.assertEqual("TestUser1", db.getPerson("TestUser1")[1])
            self.assertEqual("TestUser2", db.getPerson("TestUser2")[1])
            self.assertEqual("TestUser3", db.getPerson("TestUser3")[1])
    
if __name__ == "__main__":
    unittest.main()

