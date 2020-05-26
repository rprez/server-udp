# Sample UDP Server - Multi threaded
from socketserver import UDPServer, BaseRequestHandler,ThreadingMixIn
from NotificationDBStorageAlchemy import  NotificationDatabase
import threading
import json
import time
import os

def parseDataToJson(data):
    try:
        return json.loads(data)
    except Exception as e:
        # correccion de bug en firmware 1.63
        if "\"rssi\" : \" \"" in data:
            data = data.replace("\"rssi\" : \" \"", "\"rssi\" : \"")
            try:
                return json.loads(data)
            except Exception as e:
                pass


# Subclass the DatagramRequestHandler
# A request handler instance needs to be created.
# In case of an UDP based network server the socketserver provided class DatagramRequestHandler needs to be sub-classed and
# the handle() method to be overridden
class UDPRequestHandler(BaseRequestHandler):
    # Override the handle() method

    def handle(self):

        data = str(self.request[0], 'ascii')

        parsed_json = parseDataToJson(data)

        if parsed_json:
            # Receive and print the datagram received from client
            print(f"Request from {self.client_address[0]} Message {parsed_json}")
            NotificationDatabase.store(parsed_json)
        else:
            print(f"Error parsing json: {data}")

        # Print total thread created
        print(f"Total thread:{threading.active_count()}")


class ThreadedUDPServer(ThreadingMixIn, UDPServer):
    pass


if __name__ == "__main__":
    # Create a Server Instance
    # ThreadingUDPServer permite crear multi-threaded UDP server.

    # Create a tuple with IP Address and Port Number
    ip_addres = os.getenv("IP_ADDRESS")
    listen_port = os.getenv("LISTEN_PORT")
    if ip_addres and listen_port:
        ServerAddress = ip_addres, int(listen_port)

        UDPServerObject = ThreadedUDPServer(ServerAddress, UDPRequestHandler)
        #UDPServerObject.serve_forever()
        # Start a thread with the server -- that thread will then start one more thread for each request
        server_thread = threading.Thread(target=UDPServerObject.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True

        try:
            server_thread.start()
            print(f"Server started at {ServerAddress} ")
            while True: time.sleep(100)
        except (KeyboardInterrupt, SystemExit):
            server_thread.start()
            print("Server starting running in thread:", server_thread.name)
            UDPServerObject.shutdown()
    else:
        print(f"ENV variables IP_ADDRESS and LISTEN_PORT are not set")