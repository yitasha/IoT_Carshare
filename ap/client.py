import socket
import pickle
from getpass import getpass

class Client:
    def main(self):
        self.carid = 2
        self.HOST = "localhost"
        self.POST = 61180
        self.ADDRESS = (self.HOST, self.POST)
        self.identity()

    def identity(self):
        connCheck = ""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
                print("Connecting to {}...".format(self.ADDRESS))
                self.s.connect(self.ADDRESS)
                self.s.sendall(pickle.dumps(["Connecting", self.carid]))
                connCheck = pickle.loads(self.s.recv(4096))[0]
                print(connCheck)
                while(True):
                    if connCheck == "Car already exists":
                        break

                    print()
                    print("Home page")
                    print("1. Unlock Car")
                    print("2. Return Car")
                    print("3. Quit")
                    selection = input("Select an option: ")
                    print()

                    if selection == "1":
                        self.checkAccount(selection)
                    elif selection == "2":
                        self.checkAccount(selection)
                    elif selection == "3":
                        print("Client closed!")
                        break
                    else:
                        print("Invalid input - please try again.")
                
                print("Disconnecting from server.")
                self.s.sendall(pickle.dumps(["Disconnecting", self.carid]))
                print(pickle.loads(self.s.recv(4096))[0])
        except:
            print("Disconnecting from server.")
            pass

    def checkAccount(self, selection):
        while True:
            print()
            print("Login page")
            username = input("Enter username: ")
            password = getpass("Enter Password: ")
            print()
            message = ["Login", self.carid, username, password]
            self.s.sendall(pickle.dumps(message))
            data = pickle.loads(self.s.recv(4096))
            if data[0]:
                if selection == "1":
                    self.unlockCar(username)
                    break
                elif selection == "2":
                    self.returnCar(username)
                    break
            else:
                print("Incorrect username or password - please try again.")

    def unlockCar(self, username):
        message = ["Unlock", self.carid, username]
        self.s.sendall(pickle.dumps(message))
        print(pickle.loads(self.s.recv(4096)))
            
    def returnCar(self, username):
        message = ["Return", self.carid, username]
        self.s.sendall(pickle.dumps(message))
        print(pickle.loads(self.s.recv(4096)))

if __name__ == "__main__":
    Client().main()
