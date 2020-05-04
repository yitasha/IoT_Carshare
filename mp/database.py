import MySQLdb
import mysql.connector

class DatabaseUtils:
    HOST = "35.201.18.142"
    USER = "root"
    PASSWORD = "abc123"
    DATABASE = "People"

    def __init__(self, connection = None):
        if(connection == None):
            connection = mysql.connector.connect(DatabaseUtils.HOST, DatabaseUtils.USER,
                DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
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

    def insertPerson(self, name):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into Person (Name) values (%s)", (name,))
        self.connection.commit()

        return cursor.rowcount == 1

    def getPeople(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select PersonID, Name from Person")
            return cursor.fetchall()

    def deletePerson(self, personID):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from Person where PersonID = %s", (personID))
        self.connection.commit()
