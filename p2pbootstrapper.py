"""
Follow the instructions in each method and complete the tasks. We have given most of the house-keeping variables
that you might require, feel free to add more if needed. Hints are provided in some places about what data types 
can be used, others are left to user discretion, make sure that what you are returning from one method gets correctly
interpreted on the other end. 
"""
import socket
import threading

class p2pbootstrapper:
    def __init__(self, ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Initialize the socket object and bind it to the IP and port, refer  #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        ##############################################################################

        self.boots_socket = None
        self.clients = None  # None for now, will get updates as clients register
        
        #code added by Anna Gardner
        self.boots_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.boots_socket.bind(ip, port)
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

            #SOS idk how to start a thread rip.... but a new thread needs to be created here
            self.thread.client_thread(clientsocket, ip, port)
        #end of code added by Anna

    def client_thread(self, clientsocket, ip, port):
        ##############################################################################
        # TODO:  This function should handle the incoming connection requests from   #
        #        clients. You are free to add more arguments to this function based  #
        #        on your need                                                        #
        #        HINT: After reading the input from the buffer, you can decide what  #
        #        action needs to be done. For example, if the client wants to        #
        #        deregister, call self.deregister_client                             #
        ##############################################################################

        #code added by Anna Gardner
        self.register_client(clientsocket, ip, port)
        while True:
            data = self.boots_socket.recv()
            if data == 'deregister':
                #here compare if string sent indicates that client wants to disconnect
                self.deregister_client(clientsocket, ip, port)
            else :
               self.return_client(clientsocket)
        #end of code added by Anna

    def register_client(self, client_id, ip, port):  
        ##############################################################################
        # TODO:  Add client to self.clients                                          #
        ##############################################################################
        self.clients.append(client_id)

    def deregister_client(self, client_id):
        ##############################################################################
        # TODO:  Delete client from self.clients                                     #
        ##############################################################################
        self.clients.remove(client_id)

    def return_clients(self):
        ##############################################################################
        # TODO:  Return self.clients                                                 #
        ##############################################################################
        self.boots_socket.send(self.clients)

    def start(self):
        ##############################################################################
        # TODO:  Start timer for all clients so clients can start performing their   #
        #        actions                                                             #
        ##############################################################################
        for client in self.clients:
            client.start()
