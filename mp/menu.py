from database import DatabaseUtils

class Menu:
    def main(self):
        self.runMenu()

    def runMenu(self):
        while(True):
            print()
            print("1. List User")
            print("2. List Car")
            print("3. Insert User")
            print("4. Quit")
            selection = input("Select an option: ")
            print()

            if(selection == "1"):
                self.listPeople()
            elif(selection == "2"):
                self.listCar()
            elif(selection == "3"):
                self.insertPerson()
            elif(selection == "4"):
                print("Goodbye!")
                break
            else:
                print("Invalid input - please try again.")

    def listPeople(self):
        print("--- People ---")
        print("{:<15} {}".format("Person ID", "Name"))
        with DatabaseUtils() as db:
            for person in db.getPeople():
                print(person)
    
    def listCar(self):
        print("--- Cars ---")
        with DatabaseUtils() as db:
            for car in db.getAvailCar():
                print(car)

    def insertPerson(self):
        print("--- Insert Person ---")
        username = input("Enter username: ")
        password = input("Enter password: ")
        firstname = input("Enter firstname: ")
        lastname = input("Enter lastname: ")
        phone = input("Enter phone: ")
        email = input("Enter email: ")
        address = input("Enter address: ")

        with DatabaseUtils() as db:
            if(db.insertPerson(username, password, firstname, lastname,phone,email,address)):
                print("{} inserted successfully.".format(username))
            else:
                print("{} failed to be inserted.".format(username))

if __name__ == "__main__":
    Menu().main()
