import socket
import pickle
import datetime
from getpass import getpass
from os import listdir
from os.path import isfile, join
import cv2
import tkinter as tk
from tkinter import filedialog
import os
import sys

class Client:
    def main(self):
        """
        
        Connect to master Pi server function

        """
        # Unique car ID
        self.carid = 13

        # Socket connection 
        self.HOST = "124.189.52.217" # Shukun's Desktop
        # self.HOST = "localhost" # Test local
        # self.HOST= "101.117.248.111" # Yi's public IP
        # self.HOST= "120.21.91.201"
        self.POST = 61180
        self.ADDRESS = (self.HOST, self.POST)
        self.identity()

    def identity(self):
        """

        Main menu function

        """
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
                    # Need add in a option "Select image"
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
        """

        :param : selection
        :return: string
        """
        while True:
            while True:
                print()
                print("Login page")
                print("1. Login by image")
                print("2. Login by username and password")
                print("3. Return")
                Login = input("Select an option: ")
                print()
                Return = False

                if Login == "1":
                    # Build a list of tuples for each file type the file dialog should display
                    my_filetypes = [('all files', '.*'), ('text files', '.txt')]

                    # Ask the user to select a single file name.
                    path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                        title="Please select a file:",
                                                        filetypes=my_filetypes)

                    if path == "":
                        Return = True
                        break

                    img = cv2.imread(path,1)
                    # build message
                    time = datetime.datetime.now()
                    message = ["Login", self.carid, img, time.strftime("%Y-%m-%d")]
                    break

                elif Login == "2":
                    username = input("Enter username (Leave blank to quit) : ")
                    if(not username):
                        Return = True
                        break
                    # getpass - Hide input to protect privacy
                    password = getpass("Enter Password: ")
                    print()
                    
                    # build message
                    time = datetime.datetime.now()
                    message = ["Login", self.carid, username, password, time.strftime("%Y-%m-%d")]
                    break

                elif Login == "3":
                    Return = True
                    break

                else:
                    print("Invalid input - please try again.")

            if(Return):
                break

            # send and wait receive
            self.s.sendall(pickle.dumps(message))
            data = pickle.loads(self.s.recv(4096))
            # identity check
            if data[0]:
                # [True, (bookingid, userid, carid, cost, startdate, enddate, totalcost, status, eventid)]
                if selection == "1":
                    self.car("Unlock", data[1][0], data[1][1])
                    break
                elif selection == "2":
                    self.car("Return", data[1][0], data[1][1])
                    break
            else:
                # [False, "message"]
                print(data[1])
            
    def car(self, title, bookingid, userid):
        """

        :param username: string
        :param bookingid: int
        :return: string
        """
        time = datetime.datetime.now()
        message = [title, self.carid, bookingid, userid]
        
        # send and wait receive
        self.s.sendall(pickle.dumps(message))
        data = pickle.loads(self.s.recv(4096))

        # check message retuen
        print(data)

if __name__ == "__main__":
    Client().main()
