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
                create table user(
                    userid int NOT NULL auto_increment,
                    username text NOT NULL,
                    password text NOT NULL,
                    firstname  varchar(20) NOT NULL,
                    lastname varchar (20) NOT NULL,
                    phone varchar(15) NOT NULL,
                    email varchar (40) NOT NULL,
                    address varchar (40) NOT NULL,
                    city varchar(30) NOT NULL,
                    img text,
                    primary key (userid)
                )""")
            
            password = sha256_crypt.hash("TestPassword")
            cursor.execute("INSERT INTO user (username, password, firstname, lastname, phone, email, address, city, img) VALUES ('TestUser1', '{}', 'TestFirstName', 'TestLastName', 'TestPhone', 'TestEmail', 'TestAddress', 'TestCity', 'TestImg')".format(password))
            cursor.execute("INSERT INTO user (username, password, firstname, lastname, phone, email, address, city, img) VALUES ('TestUser2', '{}', 'TestFirstName', 'TestLastName', 'TestPhone', 'TestEmail', 'TestAddress', 'TestCity', 'TestImg')".format(password))
            cursor.execute("INSERT INTO user (username, password, firstname, lastname, phone, email, address, city, img) VALUES ('TestUser3', '{}', 'TestFirstName', 'TestLastName', 'TestPhone', 'TestEmail', 'TestAddress', 'TestCity', 'TestImg')".format(password))
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

            self.assertTrue(db.insertPerson("TestUser4", password,"TestFirstName","TestLastName","TestPhone","TestEmail","TestAddress", "TestCity"))
            self.assertTrue((count + 1) == self.countPeople())
            self.assertTrue(db.insertPerson("TestUser5", password,"TestFirstName","TestLastName","TestPhone","TestEmail","TestAddress", "TestCity"))
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
    
    # Checks user by username
    def test_getPerson(self):
        with DatabaseUtils(self.connection) as db:
            self.assertEqual("TestUser1", db.getPerson("TestUser1")[1])
            self.assertEqual("TestUser2", db.getPerson("TestUser2")[1])
            self.assertEqual("TestUser3", db.getPerson("TestUser3")[1])

    # Checks user by userid
    def test_getUser(self):
        with DatabaseUtils(self.connection) as db:
            user1 = 1
            user2 = 2
            user3 = 3
            self.assertEqual("TestUser1", db.getUser(user1)[1])
            self.assertEqual("TestUser2", db.getUser(user2)[1])
            self.assertEqual("TestUser3", db.getUser(user3)[1])

    # Compare number of users to count total database rows
    def test_getAllUsers(self):
        with DatabaseUtils(self.connection) as db:
            allusers = len(db.getAllUsers())
            self.assertEqual(allusers, self.countPeople())

    # Update user with basic details + password if neccessary
    def test_updateUser(self):
        userid = 1
        username = "TestUser1"
        password = "UpdatePass"
        firstname = "UpdateFirst"
        lastname = "UpdateLast"
        phone = "UpdatePhone"
        email = "UpdateEmail@gmail.com"
        address = "UpdateAddress"
        city = "UpdateCity"
        with DatabaseUtils(self.connection) as db:
            self.assertTrue(db.updateUser(userid, username, password, firstname, lastname, phone, email, address, city))
            # Compare data after update userid 1
            updateUser = db.getUser(userid)
            self.assertTrue(sha256_crypt.verify(password, updateUser[2]))
            self.assertEqual(updateUser[3], firstname)
            self.assertEqual(updateUser[4], lastname)
            self.assertEqual(updateUser[5], phone)
            self.assertEqual(updateUser[6], email)
            self.assertEqual(updateUser[7], address)
            self.assertEqual(updateUser[8], city)
    
    # Delete user by UserID
    def test_deleteUser(self):
        userid = 1
        count = self.countPeople()
        with DatabaseUtils(self.connection) as db:
            self.assertTrue(db.deleteUser(userid))
            # Removed 1 user so the current count should - 1
            self.assertTrue((count-1) == self.countPeople())

    
if __name__ == "__main__":
    unittest.main()

