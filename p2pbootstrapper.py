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
import json
import random

class p2pbootstrapper:
    def __init__(self, ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Initialize the socket object and bind it to the IP and port, refer  #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        ##############################################################################

        self.boots_socket = None
        self.clients = []  # None for now, will get updates as clients register
        #self.connections = []
        self.mutex = threading.Lock()
        
        #code added by Anna Gardner
        self.boots_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.boots_socket.bind((ip, port))
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
        self.boots_socket.listen(5)
        while True:
            # accept connections from outside
            (clientsocket, (ip, port)) = self.boots_socket.accept()
            #print("bootstrapper ip and port "+ip + " " + str(port))
            #self.connections.append(clientsocket)
            # length =  clientsocket.recv(4)
            # length_hdr = struct.unpack('i', length)[0]
            #print("msg length " + str(length_hdr))
            # data = clientsocket.recv(1024).decode('utf-8')
            # #print(str(type(data)))
            # data_arr = data.split(" ")
            # print(data)
            # print("bootstrapper start listening " + str(port))
            clientThread = threading.Thread(target = self.client_thread, args = (clientsocket, ip, port))#, data_arr[0], data_arr[1], data_arr[2], data_arr[3]))
            clientThread.start()
        #end of code added by Anna

    def client_thread(self, clientsocket, ip, port):#, client_id, command, ip, port):
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
            data = clientsocket.recv(1024).decode('utf-8')
            data = data.replace('"', '')
            if data:
                #print("bootstrapper data " +data[0])
                data_arr = data.split(" ")
                client_id = data_arr[0]
                data = data_arr[1]
                ip = data_arr[2]
                port = data_arr[3]
                #print("boostrapper command: "+data)
                if data == 'deregister' :
                #here compare if string sent indicates that client wants to disconnect
                    self.deregister_client(client_id)
                elif data == 'register' :
                    self.register_client(client_id, ip, port, clientsocket)
                elif data == 'sendList':
                    #print("bootstrapper sendlist")
                    client_list = self.return_clients()
                    sorted_list = sorted(client_list, key=lambda x: x[0]) 
                    toSend = json.dumps(sorted_list)
                        # var = struct.pack('i', len(toSend))
                        # clientsocket.send(var)
                    clientsocket.send(toSend.encode('utf-8'))
                     
                        #this should send nothing i think based on piazza posts
                # elif data == 'endThread':
                #     clientsocket.close()

            # length =  clientsocket.recv(4)
            # print("     length: "+str(length))
            # length_hdr = struct.unpack('i', length)[0]
            # print("msg length " + str(length_hdr))
            
        #end of code added by Anna

    def register_client(self, client_id, ip, port, clientsocket):  
        ##############################################################################
        # TODO:  Add client to self.clients                                          #
        ##############################################################################
        self.mutex.acquire()
        self.clients.append((client_id, ip, port))
        #self.connections.append(clientsocket)
        self.mutex.release()

        print("boostrapper clients")
        print("     "+json.dumps(self.clients))

    def deregister_client(self, client_id):
        ##############################################################################
        # TODO:  Delete client from self.clients                                     #
        ##############################################################################
        self.mutex.acquire()
        for client in self.clients:
            if client[0] == client_id:
                self.clients.remove(client)
        self.mutex.release()

        print("boostrapper clients deregister")
        print("     "+json.dumps(self.clients))

    def return_clients(self):
        ##############################################################################
        # TODO:  Return self.clients                                                 #
        ##############################################################################
        clients_copy = self.clients.copy()
        return clients_copy

    def start(self):
        ##############################################################################
        # TODO:  Start timer for all clients so clients can start performing their   #
        #        actions                                                             #
        ##############################################################################
        print("all clients " + json.dumps(self.clients))
        for client in self.clients:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((client[1], int(client[2])))
            client_socket.send('START'.encode('utf-8'))

            toSend = str(str(20) + ' START '+ '127.0.0.1' +' '+str(8888))
            client_socket.send(toSend.encode('utf-8'))
        #     print("connection successfull "+str(client_socket.getsockname()[1]))
        #     client_socket.send(json.dumps("START").encode('utf-8'))
        #     print("send start successfull")
        #     #time.sleep(2)
            client_socket.close()
        

