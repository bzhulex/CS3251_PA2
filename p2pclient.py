"""
Follow the instructions in each method and complete the tasks. We have given most of the house-keeping variables
that you might require, feel free to add more if needed. Hints are provided in some places about what data types 
can be used, others are left to students' discretion, make sure that what you are returning from one method gets correctly
interpreted on the other end. Most functions ask you to create a log, this is important
as this is what the auto-grader will be looking for.
Follow the logging instructions carefully.
"""

"""
Appending to log: every time you have to add a log entry, create a new dictionary and append it to self.log. The dictionary formats for diff. cases are given below
Registraion: (R)
{
    "time": <time>,
    "text": "Client ID <client_id> registered"
}
Unregister: (U)
{
    "time": <time>,
    "text": "Unregistered"
}
Fetch content: (Q)
{
    "time": <time>,
    "text": "Obtained <content_id> from <IP>#<Port>
}
Purge: (P)
{
    "time": <time>,
    "text": "Removed <content_id>"
}
Obtain list of clients known to a client: (O)
{
    "time": <time>,
    "text": "Client <client_id>: <<client_id>, <IP>, <Port>>, <<client_id>, <IP>, <Port>>, ..., <<client_id>, <IP>, <Port>>"
}
Obtain list of content with a client: (M)
{
    "time": <time>,
    "text": "Client <client_id>: <content_id>, <content_id>, ..., <content_id>"
}
Obtain list of clients from Bootstrapper: (L)
{
    "time": <time>,
    "text": "Bootstrapper: <<client_id>, <IP>, <Port>>, <<client_id>, <IP>, <Port>>, ..., <<client_id>, <IP>, <Port>>"
}
"""
import socket
import time
import json
from enum import Enum
import random
import pickle
import threading
import struct 

class Status(Enum):
            INITIAL = 0
            REGISTERED = 1
            UNREGISTERED = 2
class p2pclient:
    def __init__(self, client_id, content, actions):
        
        ##############################################################################
        # TODO: Initialize the class variables with the arguments coming             #
        #       into the constructor                                                 #
        ##############################################################################

        self.client_id = client_id
        self.content = content
        self.actions = actions  # this list of actions that the client needs to execute
        #for act in actions:
        #    print("        "+json.dumps(act))
        self.knownClients = {}

        #self.curr_time = 1

        self.content_originator_list = None  # This needs to be kept None here, it will be built eventually

        # 'log' variable is used to record the series of events that happen on the client
        # Empty list for now, update as we take actions
        # See instructions above on how to append to log
        self.log = []


        ##############################################################################
        # TODO:  You know that in a P2P architecture, each client acts as a client   #
        #        and the server. Now we need to setup the server socket of this client#
        #        Initialize the the self.socket object on a random port, bind to the port#
        #        Refer to                                                            #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        ##############################################################################

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        random.seed(client_id)
        self.port = random.randint(9000, 9999)
        self.socket.bind(('127.0.0.1', self.port))

        ##############################################################################
        # TODO:  Register with the bootstrapper by calling the 'register' function   #
        #        Make sure you communicate the server                                #
        #        port that this client is running on to the bootstrapper.            #
        ##############################################################################
        self.status = Status.INITIAL
        self.register(0)
        self.status = Status.REGISTERED
        #register may need to be adjusted here to make sure the server calls the client by the correct id?
        # data = pickle.loads(self.bootstrapperSocket.recv(1024))
        # if data == 'START':
        #     self.start()
        ##############################################################################
        # TODO:  You can set status variable based on the status of the client:      #
        #        Initial: if not yet initialized a connection to the bootstrapper    #
        #        Registered: if registered to bootstrapper                           #
        #        Unregistered: unregistred from bootstrapper, but still active       #
        #        Feel free to add more states if you need to                         #
        #        HINT: You may find enum datatype useful                             #
        ##############################################################################
        self.start()
        

    def start_listening(self):
        ##############################################################################
        # TODO:  This function will make the client start listening on the randomly  #
        #        chosen server port. Refer to                                        #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        #        You will need to link each connecting client to a new thread (using #
        #        client_thread function below) to handle the requested action.       #
        ##############################################################################
        #code added by Anna Gardner
        self.socket.listen()
        while True:
            # accept connections from outside
            (clientsocket, (ip, port)) = self.socket.accept()
            #print("     client ip and port "+ip + " " + str(port))
            clientThread = threading.Thread(target = self.client_thread, args = (clientsocket, ip, port))
            clientThread.start()
        #end of code added by Anna

    def client_thread(self, clientsocket, ip, port):
        ##############################################################################
        # TODO:  This function should handle the incoming connection requests from   #
        #        other clients.You are free to add more arguments to this function   #
        #        based your need                                                     #
        #        HINT: After reading the input from the buffer, you can decide what  #
        #        action needs to be done. For example, if the client is requesting   #
        #        list of known clients, you can return the output of self.return_list_of_known_clients #
        ##############################################################################
        
        while True:
            data = clientsocket.recv(1024).decode('utf-8')
            #print("data "+data)
            #O, S, M commands
            #hint stuff
            if data :
                if data == "START":
                    self.start()
                if data == 'knownClientsPlease' :
                #here compare if string sent indicates that client wants to disconnect
                    clientsocket.send(json.dumps(self.return_list_of_known_clients()).encode('utf-8'))
                elif data == 'contentList' :
                    clientsocket.send(json.dumps(self.return_content_list()).encode('utf-8'))


    def register(self, curr_time,  ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Register with the bootstrapper. Make sure you communicate the server#
        #        port that this client is running on to the bootstrapper.            #
        #        Append an entry to self.log that registration is successful         #
        ##############################################################################
        if self.status == Status.INITIAL:
            bootstrapperSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bootstrapperSocket.connect((ip, port))
            #data = pickle.loads(clientsocket.recv())
            #self.client_id = data
            toSend = str(str(self.client_id) + ' register '+ str(ip) +' '+str(self.port))
            bootstrapperSocket.send(json.dumps(toSend).encode('utf-8'))
            bootstrapperSocket.close()
            if curr_time != 0:
                register_dict = {}
                register_dict["time"] = self.curr_time
                register_dict["text"] = str("Client ID " +str(self.client_id)+" registered")
                self.log.append(register_dict)
    

    def deregister(self, curr_time, ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Deregister with the bootstrapper                                    #
        #        Append an entry to self.log that deregistration is successful       #
        ##############################################################################
        bootstrapperSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bootstrapperSocket.connect((ip, port))
        toSend = str(str(self.client_id) + ' deregister '+ str(ip) +' '+str(self.port))
        # var = struct.pack('i', len(toSend))
        # self.bootstrapperSocket.send(var)
        bootstrapperSocket.send(json.dumps(toSend).encode('utf-8'))
        bootstrapperSocket.close()
        dereg_dict = {}
        dereg_dict["time"] = curr_time
        dereg_dict["text"] = "Unregistered"
        self.log.append(dereg_dict)

        #print("DEREGISTER FINISHED")

    def start(self):
        ##############################################################################
        # TODO:  The Bootstrapper will call this method of the client to indicate    #
        #        that it needs to start its actions. Once this is called, you have to#
        #        start reading the items in self.actions and start performing them   #
        #        sequentially, at the time they have been scheduled for.             #
        #        HINT: You can use time library to schedule these.                   #
        ##############################################################################

        ##############################################################################
        # TODO:  ***IMPORTANT***                                                     #
        # At the end of your actions, “export” self.log to a file: client_x.json,    #
        # this is what the autograder is looking for. Python’s json package should   #
        # come handy.                                                                #
        ##############################################################################
        
        #set time to zero
        start = time.time()
        action_num = 0
        while action_num < len(self.actions):
            time_diff = time.time() - start
            
            if self.actions[action_num]["time"] < time_diff:
            #perform action -> somehow parse it from this actions input
                curr_time = self.actions[action_num]["time"] 
                #print("ACTION NUM: "+str(action_num) + "CURR TIME " + str(curr_time))
                code = self.actions[action_num]["code"]
                if code == "R":
                    self.register(curr_time)
                elif code == "U":
                    self.deregister(curr_time)
                elif code == "Q":
                    self.request_content(self.actions[action_num]["content_id"], curr_time)
                elif code == "P":
                    self.purge_content(self.actions[action_num]["content_id"], curr_time)    
                elif code == "O":
                    self.query_client_for_known_client(self.actions[action_num]["client_id"], curr_time)
                elif code == "M":
                    self.query_client_for_content_list(self.actions[action_num]["client_id"], curr_time)
                elif code == "L":
                    self.query_bootstrapper_all_clients(curr_time)
                action_num += 1
            
                
        string = "client_" + str(self.client_id) + ".json"
        outfile = open(string, "w")
        json.dump(json.dumps(self.log), outfile)
        outfile.close()


    def query_bootstrapper_all_clients(self, curr_time, ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Use the connection to ask the bootstrapper for the list of clients  #
        #        registered clients.                                                 #
        #        Append an entry to self.log                                         #
        ##############################################################################
        #print("     start query_bootstrapper_all_clients")
        while self.status == Status.INITIAL:
            pass
        bootstrapperSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bootstrapperSocket.connect((ip, port))
        toSend = str(str(self.client_id) + ' sendList '+ '127.0.0.1' +' '+str(self.port))
        # var = struct.pack('i', len(toSend))
        # self.bootstrapperSocket.send(var)
        bootstrapperSocket.send(json.dumps(toSend).encode('utf-8'))
        #print("     sendList flag sent")
        # length = self.bootstrapperSocket.recv(4)
        # length_hdr = struct.unpack('i', length)[0]
        data = bootstrapperSocket.recv(1048).decode('utf-8')
        bootstrapperSocket.close()
        toReturn = json.loads(data)
        #print("     query all clients "+json.dumps(toReturn))
        var = '<'
        for client in toReturn:
            var += '<'
            for piece in client:
                var += str(piece)+','
            var += ">"
        var += '>'
        q_dict = {}
        q_dict['time'] = curr_time
        q_dict['text'] = "Bootstrapper "+var
        self.log.append(q_dict)
        return toReturn

    def query_client_for_known_client(self, curr_time, client_id, ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Connect to the client and get the list of clients it knows          #
        #        Append an entry to self.log                                         #
        ##############################################################################
        all_clients = self.query_bootstrapper_all_clients(curr_time)
        ip = None
        port = 0
        for client in all_clients:
            if client[0] == client_id:
                right_client = client
                ip = client[1]
                port = client[2]

        #(ip, port) = self.knownClients.get(client_id)
        # clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # clientSocket.connect((ip, port))
        # clientSocket.send(pickle.dumps('knownClientsPlease'))
        # knownClientsDict = pickle.loads(clientSocket.recv(1024))
        # q_dict = {}
        # q_dict["time"] = curr_time
        # q_dict["text"] = str("Client "+str(client_id)+" "+json.dumps(knownClientsDict))
        # self.log.append(q_dict)
        # return knownClientsDict


    def return_list_of_known_clients(self):
        ##############################################################################
        # TODO:  Return the list of clients known to you                             #
        #        HINT: You could make a set of <IP, Port> from self.content_originator_list #
        #        and return it.                                                      #
        ##############################################################################
        #could iterate over content originator list adn get ip and port numbers
        #return self.knownClients.copy()
        pass

    def query_client_for_content_list(self, client_id, curr_time):
        ##############################################################################
        # TODO:  Connect to the client and get the list of content it has            #
        #        Append an entry to self.log                                         #
        ##############################################################################
        all_clients = self.query_bootstrapper_all_clients(curr_time)
        ip = None
        port = 0
        for client in all_clients:
            if client[0] == client_id:
                right_client = client
                ip = client[1]
                port = client[2]

        # clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # clientSocket.connect((ip, port))
        # clientSocket.send(pickle.dumps('contentList'))
        # knownContentList = clientSocket.recv(pickle.load())
        # q_dict = {}
        # q_dict["time"] = curr_time
        # q_dict["text"] = str("Client "+str(client_id)+''.join(knownContentList))
        # return knownContentList


    def return_content_list(self, curr_time):
        ##############################################################################
        # TODO:  Return the content list that you have (self.content)                #
        ##############################################################################
        pass
        # col = [i[0] for i in self.content_originator_list]
        # temp = [i for i in self.content if i in col ]
        # return self.content_originator_list.copy()

    def request_content(self, content_id, curr_time):
        #####################################################################################################
        # TODO:  Your task is to obtain the content and append it to the                                    #
        #        self.content list.  To do this:                                                            #
        #        The program will first query the bootstrapper for a set                                    #
        #        of all clients. Then start sending requests for the content to each of these clients in a  #
        #        serial fashion. From any P2Pclient, it might either receive the content, or may receive    #
        #        a hint about where the content might be located. On receiving an hint, the client          #
        #        attempts that P2Pclient before progressing ahead with its current list. If content is      #
        #        not found, then it proceeds to request every P2PClient for a list of all other clients it  #
        #        knows and creates a longer list for trying various P2PClients. You can use the above query #
        #        methods to help you in fetching the content.                                               #
        #        Make sure that when you are querying different clients for the content you want, you record#
        #        their responses(hints, if present) appropriately in the self.content_originator_list       #
        #        Append an entry to self.log that content is obtained                                       #
        #####################################################################################################
        #do .sends in here
        #go though each client and send the content id
        #   each client will check in it's own content for the content ID
        #   if not each clinet will check its COL 
        #   if none of that send a NO
        #   if you get a NO go to next client
        #   if you get a hint then jump to next client
        #   when tou get the data log it an append 
        # bootstrapperClients = self.query_bootstrapper_all_clients()
        # for client in bootstrapperClients:
        #     self.knownClients.update({client, bootstrapperClients.get(client)})
        # for client in bootstrapperClients:
        #     clientContentList = self.query_client_for_content_list(client)
        #     for content in clientContentList:
        #         if content == content_id:
        #             self.content.append(content_id)
        #             self.content_originator_list.update({content_id: self.knownClients.get(client)})
        #             q_dict = {}
        #             q_dict["time"] = self.curr_time
        #             q_dict["text"] = str("Obtained "+str(content_id)+" from "+str(self.knownClients.get(client)))
        #             self.log.append(q_dict)
        #             return
        # for client in bootstrapperClients:
        #     clientKnownContacts = self.query_client_for_known_client(client)
        #     for clientclient in clientKnownContacts:
        #         if self.knownClients.get(client) == None :
        #             self.knownClients.update({clientclient: clientKnownContacts.get(clientclient)})
        #             clientclientContentList = self.query_client_for_content_list(clientclient)
        #             for contentboi in clientclientContentList:
        #                 if contentboi == content_id:
        #                     self.content.append(content_id)
        #                     self.content_originator_list.update({content_id: self.knownClients.get(clientclient)})
        #                     q_dict = {}
        #                     q_dict["time"] = self.curr_time
        #                     q_dict["text"] = str("Obtained "+str(content_id)+" from "+str(self.knownClients.get(client)))
        #                     self.log.append(q_dict)
        #                     return
        pass

    def purge_content(self, content_id, curr_time):
        #####################################################################################################
        # TODO:  Delete the content from your content list                                                  #
        #        Append an entry to self.log that content is purged                                         #
        #####################################################################################################
        # self.content.remove(content_id)
        purge_dict = {}
        purge_dict["time"] = curr_time
        purge_dict["text"] = str("Removed "+str(content_id))
