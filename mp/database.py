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
    #Why this function is a Boolean: True or False
    def insertPerson(self, username, password, firstname, lastname,phone,email,address):
        with self.connection.cursor() as cursor:
            sql = "insert into user (username, password, firstname, lastname, phone, email, address) values (%s, %s, %s, %s, %s, %s, %s)"
            val = (username, password, firstname, lastname, phone, email, address)
            cursor.execute(sql, val)
        self.connection.commit()
        return cursor.rowcount == 1

    def checkPerson(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from user where username = '{}'".format(username))
            results = cursor.fetchone()
            userpass = results[2]
            if (sha256_crypt.verify(password, userpass)):
                return True
            else:
                return False

    def getPerson(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from user where username = '{}'".format(username))
            return cursor.fetchone()

    def getPeople(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from user")
            return cursor.fetchall()

    def deletePerson(self, personID):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from Person where PersonID = %s", (personID))
        self.connection.commit()
