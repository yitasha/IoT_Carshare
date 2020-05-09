import socket
import pickle
from getpass import getpass

class Client:
    def main(self):
        self.HOST = "localhost"
        self.POST = 61180
        self.ADDRESS = (self.HOST, self.POST)
        self.identity()

    def identity(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            print("Connecting to {}...".format(self.ADDRESS))
            self.s.connect(self.ADDRESS)
            print("Connected.")

            while(True):
                print()
                print("Home page")
                print("1. Has an account")
                print("2. Create a new account")
                print("3. Quit")
                selection = input("Select an option: ")
                print()

                if(selection == "1"):
                    self.checkAccount()
                elif(selection == "2"):
                    self.createAccount()
                elif(selection == "3"):
                    print("Client closed!")
                    break
                else:
                    print("Invalid input - please try again.")
            
            self.s.sendall(pickle.dumps(["END"]))
            print("Disconnecting from server.")

    def checkAccount(self):
        while True:
            print()
            print("Login page")
            username = input("Enter username: ")
            password = getpass("Enter Password: ")
            print()
            message = ["Login", username, password]
            self.s.sendall(pickle.dumps(message))
            data = pickle.loads(self.s.recv(4096))
            if data:
                self.function(username)
                break
            else:
                print("Incorrect username or password - please try again.")

    def createAccount(self):
        while True:
            print()
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            firstname = input("Enter firstname: ")
            lastname = input("Enter lastname: ")
            phone = input("Enter phone: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            print()
            message = ["Create", username, password, firstname, lastname, phone, email, address]
            self.s.sendall(pickle.dumps(message))
            data = pickle.loads(self.s.recv(4096))
            if data:
                print(data[1])
                self.checkAccount()
                break
            else:
                print(data[1])

    def function (self, user):
        while(True):
            print()
            print("Welcome {}.".format(user))
            print("1. Unlock Car")
            print("2. Return Car")
            print("3. Logout")
            selection = input("Select an option: ")
            print()

            if(selection == "1"):
                self.unlockCar()
            elif(selection == "2"):
                self.returnCar()
            elif(selection == "3"):
                print("Goodbye {}!".format(user))
                break
            else:
                print("Invalid input - please try again.")

    def unlockCar(self):
        print("Unlock Car")
            
    def returnCar(self):
        print("Return Car")

if __name__ == "__main__":
    Client().main()
