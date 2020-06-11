#!/usr/bin/env python3
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
import bluetooth
import time
import zxing

class Client:
    def main(self):
        """
        
        Connect to master Pi server function

        """
        # Unique car ID
        self.carid = 1

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

                    # Check the car status
                    self.s.sendall(pickle.dumps(["Status", self.carid]))
                    StatusCheck = pickle.loads(self.s.recv(4096))
                    print("Car status - {}".format(StatusCheck))

                    if StatusCheck == "Faulty":
                        # If car status is faulty
                        # Automatically enter engineer mode
                        selection = "Engineer"
                    else:
                        selection = ""

                    # Main menu
                    # Need add in a option "Select image"
                    if selection == "":
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
                    elif selection == "Engineer":
                        self.bluetoothSearch()
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

    def bluetoothSearch(self):
        # Get engineer all devices
        message = ["CheckEngineerDevices"]
        self.s.sendall(pickle.dumps(message))
        Engineer_devices = pickle.loads(self.s.recv(4096))
        print(Engineer_devices)
        counter = 0
        Search = True
        while Search:
            # Automatically scan the nearby devices
            print("Performing inquiry...")
            counter += 1
            nearby_devices = bluetooth.discover_devices(duration=8,
                                            lookup_names=True,
                                            flush_cache=True,
                                            lookup_class=False)
            print("Found {} devices".format(len(nearby_devices)))
            print(counter)
            for addr, name in nearby_devices:
                try:
                    print("   {} - {}".format(addr, name))
                except UnicodeEncodeError:
                    print("   {} - {}".format(addr, name.encode("utf-8", "replace")))
            
            for addr, name in nearby_devices:
                if addr in Engineer_devices:
                    self.checkEngineerIdentity()
                    Search = False
                    break
            
            if counter > 2:
                self.s.sendall(pickle.dumps(["Disconnecting", self.carid]))
                os._exit(0)
    
    def checkEngineerIdentity(self):
        while True:
            print()
            print("Engineer mode")
            print("1. Login by QR code")
            print("2. Login by username and password")
            print("3. Return")
            EngineerInput = input("Select an option: ")
            print()

            if EngineerInput == "1":
                self.checkEngineerInput(EngineerInput)
            elif EngineerInput == "2":
                self.checkEngineerInput(EngineerInput)
            elif EngineerInput == "3":
                break
            else:
                print("Invalid input - please try again.")

    def checkEngineerInput(self, EngineerInput):
        while True:
            if EngineerInput == "1":
                # Login by QR code
                reader = zxing.BarCodeReader()
                # Build a list of tuples for each file type the file dialog should display
                my_filetypes = [('all files', '.*'), ('text files', '.txt')]
                # Ask the user to select a single file name.
                path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                    title="Please select a file:",
                                                    filetypes=my_filetypes)
                if path == "":
                    break
                # decode QR
                barcode = reader.decode(path)
                username = barcode.parsed.split(', ')[0]
                password = barcode.parsed.split(', ')[1]
                message = ["CheckEngineerIdentity", username, password, self.carid]

            elif EngineerInput == "2":
                # Login by username and password
                username = input("Enter username (Leave blank to quit) : ")
                if(not username):
                    return
                password = getpass("Enter Password: ")
                message = ["CheckEngineerIdentity", username, password, self.carid]

            # Receive login reply
            self.s.sendall(pickle.dumps(message))
            data = pickle.loads(self.s.recv(4096))
            if data[0] == "True":
                # True
                message = ["Repair", self.carid]
                self.s.sendall(pickle.dumps(message))
                data = pickle.loads(self.s.recv(4096))
                # Send and Receive Repair reply
                if data[0] == "True":
                    # True
                    print()
                    print("Start repairing the car")
                    time.sleep(2)
                    print()
                    print("The car has been repaired")
                    return
                else:
                    # False
                    print()
                    print("The car does not need to be repaired")
                    return
            else:
                # False
                print("Username or Password is incorrect")

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
