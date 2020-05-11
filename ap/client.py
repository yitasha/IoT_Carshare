import socket
import pickle
import datetime
from getpass import getpass

class Client:
    def main(self):
        # Unique car ID
        self.carid = 2

        # Socket connection 
        # self.HOST = "192.168.0.135"
        self.HOST = "localhost"
        self.POST = 61180
        self.ADDRESS = (self.HOST, self.POST)
        self.identity()

    def identity(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
                print("Connecting to {}...".format(self.ADDRESS))
                # Socket connect
                self.s.connect(self.ADDRESS)

                # Connect and send connection test through socket
                # message [type, carid]
                self.s.sendall(pickle.dumps(["Connecting", self.carid]))

                # Receive the reply via socket
                connCheck = pickle.loads(self.s.recv(4096))[0]
                # Result is "Connected" or "Car already exists" 
                print(connCheck)

                while(True):
                    # Break is to prevent multiple logins of the same carid
                    if connCheck == "Car already exists":
                        break

                    # Main menu
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
                
                # Out of loop is disconnect
                print("Disconnecting from server.")

                # Send final message [type, carid]
                self.s.sendall(pickle.dumps(["Disconnecting", self.carid]))
                # Recive final message ["Disconnected"] end loop
                print(pickle.loads(self.s.recv(4096))[0])
        except:
            # Situation: The server is suddenly disconnected
            print("Disconnecting from server.")
            pass

    def checkAccount(self, selection):
        while True:
            print()
            print("Login page")
            username = input("Enter username (Leave blank to quit) : ")
            # getpass - Hide input to protect privacy
            password = getpass("Enter Password: ")
            print()

            if(not username):
                break

            time = datetime.datetime.now()
            message = ["Login", self.carid, username, password, time.strftime("%Y-%m-%d")]
            # send and wait receive
            self.s.sendall(pickle.dumps(message))
            data = pickle.loads(self.s.recv(4096))

            # identity check
            if data[0]:
                # [True, (bookingid, userid, carid, cost, startdate, enddate, totalcost, status, eventid)]
                if selection == "1":
                    self.unlockCar(username, data[1][0])
                    break
                elif selection == "2":
                    self.returnCar(username, data[1][0])
                    break
            else:
                # [False, "message"]
                print(data[1])

    def unlockCar(self, username, bookingid):
        time = datetime.datetime.now()
        message = ["Unlock", self.carid, username, bookingid, time.strftime("%Y-%m-%d")]

        # send and wait receive
        self.s.sendall(pickle.dumps(message))
        data = pickle.loads(self.s.recv(4096))

        # Unlock check message retuen
        print(data)
            
    def returnCar(self, username, bookingid):
        time = datetime.datetime.now()
        message = ["Return", self.carid, username, bookingid, time.strftime("%Y-%m-%d")]
        
        # send and wait receive
        self.s.sendall(pickle.dumps(message))
        data = pickle.loads(self.s.recv(4096))

        # Return check message retuen
        print(data)

if __name__ == "__main__":
    Client().main()
