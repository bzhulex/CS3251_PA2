"""
Follow the instructions in each method and complete the tasks. We have given most of the house-keeping variables
that you might require, feel free to add more if needed. Hints are provided in some places about what data types 
can be used, others are left to user discretion, make sure that what you are returning from one method gets correctly
interpreted on the other end. 
"""
import socket
import threading
import sys
import pickle

#TODO: mutex lock self.clients and client counter for race conditions dict since multiple threads access it

class p2pbootstrapper:
    def __init__(self, ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Initialize the socket object and bind it to the IP and port, refer  #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        ##############################################################################

        self.boots_socket = None
        self.clients = {}  # None for now, will get updates as clients register
        self.client_id_counter = 0
        self.clients_lock = threading.Lock()
        
        #code added by Anna Gardner
        self.boots_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.boots_socket.bind((ip, port))
        self.start_listening()
        #end of code added by Anna


    def start_listening(self):
        ##############################################################################
        # TODO:  This function will make the BS start listening on the port 8888     #
        #        Refer to                                                            #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        #        You will need to link each connecting client to a new thread (using #
        #        client_thread function below) to handle the requested action.       #
        ##############################################################################

        #code added by Anna Gardner
        self.boots_socket.listen()
        while True:
            # accept connections from outside
            (clientsocket, (ip, port)) = self.boots_socket.accept()

            clientThread = threading.Thread(target = self.client_thread, args = (clientsocket, ip, port))
            clientThread.start()
        #end of code added by Anna

    def client_thread(self, clientsocket, client_id, ip, port):
        ##############################################################################
        # TODO:  This function should handle the incoming connection requests from   #
        #        clients. You are free to add more arguments to this function based  #
        #        on your need                                                        #
        #        HINT: After reading the input from the buffer, you can decide what  #
        #        action needs to be done. For example, if the client wants to        #
        #        deregister, call self.deregister_client                             #
        ##############################################################################

        #code added by Anna Gardner
        #clientsocket.send(pickle.dumps(clientsocket))
        while True :
            data = pickle.load(clientsocket.recv())
            if data :
                if data == 'deregister' :
                #here compare if string sent indicates that client wants to disconnect
                    self.deregister_client(clientsocket)
                elif data == 'register' :
                    self.register_client(client_id, ip, port)
                elif data == 'sendList':
                    clientDict = self.return_clients
                    if len(clientDict) > 0 :
                        binaryClientDict = pickle.dumps()
                        clientsocket.send(binaryClientDict)
                    else: 
                        #this should send nothing i think based on piazza posts
                        clientsocket.send(binaryClientDict)
                elif data == 'endThread':
                    clientsocket.close()
        
        #end of code added by Anna

    def register_client(self, client_id, ip, port):  
        ##############################################################################
        # TODO:  Add client to self.clients                                          #
        ##############################################################################
        self.client_id_counter += 1
        self.clients.update({client_id: (ip, port)})

    def deregister_client(self, client_id):
        ##############################################################################
        # TODO:  Delete client from self.clients                                     #
        ##############################################################################
        self.clients.pop(client_id)

    def return_clients(self):
        ##############################################################################
        # TODO:  Return self.clients                                                 #
        ##############################################################################
        return self.clients.copy()

    def start(self):
        ##############################################################################
        # TODO:  Start timer for all clients so clients can start performing their   #
        #        actions                                                             #
        ##############################################################################
        for client in self.clients:
            client.start()

