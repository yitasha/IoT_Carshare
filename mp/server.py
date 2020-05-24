import socket
import threading
import pickle
from database import DatabaseUtils

class Server:
    def main(self):
        """

        Server records the connected carid
        
        run server

        """
        # Server records the connected carid
        self.connectList = []

        # run server
        self.run()

    def run(self):
        """

        Socket Listen

        """
        # Socket Listen
        # HOST = "192.168.0.135" # Shukun's Pi
        HOST = "192.168.0.102" # Shukun's Desktop
        # HOST = "localhost" # Test local
        POST = 61180
        ADDRESS = (HOST, POST)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(ADDRESS)
            s.listen()
            print("Listening on {}...".format(ADDRESS))
            while True:
                # Loop for multiple clients
                # When the client is connected, through multi-threaded processing
                conn, addr = s.accept()
                t = threading.Thread(target=self.threadHandle, args=(conn, addr))
                # Start a new thread for the client and return to the loop to wait for the next client
                t.start()
            
    def threadHandle(self, conn, addr):
        """

        :param conn:
        :param addr:
        :return:
        """
        try:
            with conn:
                while True:
                    # Receive and reply messages in a loop
                    # Messages is list [message type, carid, ...]
                    messages = pickle.loads(conn.recv(4096))

                    # Messages return results through case processing
                    # reply = ["message"]
                    reply = self.messagesCase(messages)


                    if reply[0] == "Disconnected" or reply[0] == "Car already exists":
                        conn.sendall(pickle.dumps(reply))
                        break
                    else:
                        conn.sendall(pickle.dumps(reply))
        except:
            # Situation: The client is suddenly disconnected
            # Clear this carid record for next time connecting
            print("Disconnected to car id: {}".format(messages[1]))
            self.connectList.remove(messages[1])
            pass

    def messagesCase(self, list):
        """

        Case Messages ["Login", carid, username, password, date]

        :param list: string
        :return: string
        """
        # case Messages ["Login", carid, username, password, date]
        if list[0] == "Login":
            # in Database checkLogin_AP(self, username, password, carid, date):
            reply = DatabaseUtils().checkLogin_AP(list[2], list[3], list[1], list[4])
            print("Client {} try to login car id {} and reply {}".format(list[2], list[1], reply[0]))
            return reply
        
        # case Messages ["Unlock", carid, username, bookingid]
        elif list[0] == "Unlock":
            # in Database unlock_AP(self, bookingid):
            reply = [DatabaseUtils().unlock_AP(list[3])]
            print("Client {} try to unlock car id {} and reply {}".format(list[2], list[1], reply[0]))
            return reply
        
        # case Messages ["Return", carid, username, bookingid]
        elif list[0] == "Return":
            # in Database return_AP(self, bookingid):
            reply = [DatabaseUtils().return_AP(list[3])]
            print("Client {} try to return car id {} and reply {}".format(list[2], list[1], reply[0]))
            return reply

        # case Messages ["Connecting", carid]
        elif list[0] == "Connecting":
            # carid not in server connected record
            if list[1] not in self.connectList:
                # Server print carid connected
                print("Connected to car id: {}".format(list[1]))
                # Add carid in connected record list
                self.connectList.append(list[1])
                reply = ["Connected"]
            # carid already in server connected record
            else:
                reply = ["Car already exists"]
            return reply
        
        # case Messages ["Disconnecting", carid]
        elif list[0] == "Disconnecting":
            print("Disconnected to car id: {}".format(list[1]))
            # Clear this carid record for next time connecting
            self.connectList.remove(list[1])
            reply = ["Disconnected"]
            return reply

if __name__ == "__main__":
    Server().main()
