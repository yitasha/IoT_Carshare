import socket
import threading
import pickle
from database import DatabaseUtils

class Server:
    def main(self):
        self.connectList = []
        self.run()

    def run(self):
        HOST = "localhost"
        POST = 61180
        ADDRESS = (HOST, POST)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(ADDRESS)
            s.listen()
            print("Listening on {}...".format(ADDRESS))
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=self.threadHandle, args=(conn, addr))
                t.start()
            
    def threadHandle(self, conn, addr):
        try:
            with conn:
                while True:
                    data = pickle.loads(conn.recv(4096))
                    reply = self.dataCase(data)
                    if reply[0] == "Disconnected" or reply[0] == "Car already exists":
                        conn.sendall(pickle.dumps(reply))
                        break
                    else:
                        conn.sendall(pickle.dumps(reply))
        except:
            print("Disconnected to car id: {}".format(data[1]))
            self.connectList.remove(data[1])
            pass

    def dataCase(self, list):
        if list[0] == "Login":
            reply = [DatabaseUtils().checkPerson(list[2], list[3])]
            print("Client {} try to login car id {} and reply {}".format(list[2], list[1], reply[0]))
            return reply
            
        elif list[0] == "Unlock":
            reply = ["Unlock", DatabaseUtils().showBooking(DatabaseUtils().getPerson(list[2])[0])]
            print("Client {} try to unlock car id {}".format(list[2], list[1]))
            return reply
        
        elif list[0] == "Return":
            reply = ["Return"]
            print("Client {} try to return car id {}".format(list[2], list[1]))
            return reply

        elif list[0] == "Connecting":
            if list[1] not in self.connectList:
                print("Connected to car id: {}".format(list[1]))
                self.connectList.append(list[1])
                reply = ["Connected"]
            else:
                reply = ["Car already exists"]
            return reply
        
        elif list[0] == "Disconnecting":
            print("Disconnected to car id: {}".format(list[1]))
            self.connectList.remove(list[1])
            reply = ["Disconnected"]
            return reply

if __name__ == "__main__":
    Server().main()
