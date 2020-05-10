import socket
import threading
import pickle
from database import DatabaseUtils

class Server:
    def main(self):
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
        with conn:
            print("Connected to {}".format(addr))

            while True:
                data = pickle.loads(conn.recv(4096))
                reply = self.dataCase(data, addr)
                if(reply[0] == "END"):
                    break
                conn.sendall(pickle.dumps(reply))
            
            print("Disconnecting from {}".format(addr))

    def dataCase(self, list, addr):
        if list[0] == "Login":
            reply = [DatabaseUtils().checkPerson(list[1], list[2])]
            print("{} Try to login and reply {}".format(addr, reply[0]))
            return reply

        elif list[0] == "Create":
            reply = [DatabaseUtils().checkUsername(list[1])]
            if reply[0]:
                reply.clear
                reply = [DatabaseUtils().insertPerson(list[1], list[2], list[3], list[4], list[5], list[6], list[7])]
                if reply[0]:
                    reply.insert(1, "{} register successfully. try to login.".format(list[1]))
                else:
                    reply.insert(1, "{} failed to register.".format(list[1]))
            else:
                reply.insert(1, "{} already exist, try a different one.".format(list[1]))
            print("{} Try to Create an account and reply {}".format(addr, reply[0]))
            return reply
            
        elif list[0] == "END":
            reply = ["END"]
            return reply

if __name__ == "__main__":
    Server().main()
