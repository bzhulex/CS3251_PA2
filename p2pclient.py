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

        #self.curr_time = 1

        self.content_originator_list = None  # This needs to be kept None here, it will be built eventually
        self.content_originator_list = {}

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
        time.sleep(.1)
        self.p2pclientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        random.seed(client_id)
        self.port = random.randint(9000, 9999)
        self.p2pclientsocket.bind(('127.0.0.1', self.port))

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
        #self.start()
        

    def start_listening(self):
        ##############################################################################
        # TODO:  This function will make the client start listening on the randomly  #
        #        chosen server port. Refer to                                        #
        #        https://docs.python.org/3/howto/sockets.html on how to do this.     #
        #        You will need to link each connecting client to a new thread (using #
        #        client_thread function below) to handle the requested action.       #
        ##############################################################################
        #code added by Anna Gardner
        self.p2pclientsocket.listen()
        while True:
            # accept connections from outside
            #print('listening')
            (clientsocket, (ip, port)) = self.p2pclientsocket.accept()
            #print('accepted')
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
            data = data.replace('"', '')
            if data:
                print("~~~~~p2pclient_thread data: " +data)
                data_arr = data.split(" ")
                #client_id = data_arr[0]
                data = data_arr[1]
                ip = data_arr[2]
                port = data_arr[3]
                if data == 'START':
                    #print('start was called')
                    self.start()
                if data == 'knownClientsPlease' :
                    client_list = self.return_list_of_known_clients() 
                    toSend = json.dumps(client_list)
                    clientsocket.send(toSend.encode('utf-8'))
                elif data == 'contentList' :
                    content_list = self.return_content_list()
                    #sorted_list = sorted(content_list, key=lambda x: x[0]) 
                    toSend = json.dumps(content_list)
                    print("~~~~~got send content list flag sending: "+ str(self.client_id) +" " +toSend)
                    clientsocket.send(toSend.encode('utf-8'))


    def register(self, curr_time,  ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Register with the bootstrapper. Make sure you communicate the server#
        #        port that this client is running on to the bootstrapper.            #
        #        Append an entry to self.log that registration is successful         #
        ##############################################################################
        #if self.status == Status.INITIAL:
        bootstrapperSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bootstrapperSocket.connect((ip, port))
            #data = pickle.loads(clientsocket.recv())
            #self.client_id = data
        toSend = str(str(self.client_id) + ' register '+ str(ip) +' '+str(self.port))
        bootstrapperSocket.send(toSend.encode('utf-8'))
        bootstrapperSocket.close()
        if curr_time != 0:
            register_dict = {}
            register_dict["time"] = curr_time
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
        bootstrapperSocket.send(toSend.encode('utf-8'))
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
        # At the end of your actions, ???export??? self.log to a file: client_x.json,    #
        # this is what the autograder is looking for. Python???s json package should   #
        # come handy.                                                                #
        ##############################################################################
        
        start = time.time()
        action_num = 0
        while action_num < len(self.actions):
            while_start = time.time()
            # while self.actions[action_num]["time"] < time_diff:
            #     pass
            curr_time = self.actions[action_num]["time"]
            print("CLIENT "+ str(self.client_id)+" ACTION NUM: "+str(action_num) + " CODE: " + self.actions[action_num]["code"]+ " CURR TIME " + str(curr_time))
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
                #print("time: "+str(curr_time)+" client "+ str(self.client_id) + " O: query_client_for_known_client "+ str(self.actions[action_num]["client_id"]))
                self.query_client_for_known_client(self.actions[action_num]["client_id"], curr_time)
            elif code == "M":
                #print("time: "+str(curr_time)+" client "+ str(self.client_id) + " M: query_client_for_content_list "+ str(self.actions[action_num]["client_id"]))
                self.query_client_for_content_list(self.actions[action_num]["client_id"], curr_time)
            elif code == "L":
                self.query_bootstrapper_all_clients(curr_time)
            action_num += 1
            while_end = time.time()
            time.sleep(1.5 - (while_end-while_start))
                
        string = "client_" + str(self.client_id) + ".json"
        outfile = open(string, "w")
        json.dump(self.log, outfile)
        outfile.close()

    # def clean_client_list(self, toReturn):
    #     count  = 0
    #     var = '<'
    #     for client in toReturn:
    #         var += '<'
    #         for i in range(len(client)):
    #             piece = client[i]
    #             if i < len(client) - 1:
    #                 var += str(piece)+', '
    #             else:
    #                 var += str(piece)
    #             i += 1 
    #         if count < len(toReturn) - 1:
    #             var += ">, "
    #         else:
    #             var += ">"
    #         count += 1
    #     var += '>'
    #     return var    

    def query_bootstrapper_all_clients(self, curr_time, log = True, ip='127.0.0.1', port=8888):
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
        bootstrapperSocket.send(toSend.encode('utf-8'))
        #print("     sendList flag sent")
        # length = self.bootstrapperSocket.recv(4)
        # length_hdr = struct.unpack('i', length)[0]
        data = bootstrapperSocket.recv(1048).decode('utf-8')
        bootstrapperSocket.close()
        clientDataToList = json.loads(data)
        newData = data.replace('[','<').replace(']','>').replace('\"','')
        newestData = newData[1:len(newData)-1]
        if log:
            q_dict = {}
            q_dict['time'] = curr_time
            q_dict['text'] = "Bootstrapper: "+newestData
            #print("     query all clients id: "+str(self.client_id)+ " "+var)
            self.log.append(q_dict)
        return clientDataToList

    def query_client_for_known_client(self, client_id, curr_time, log = True, ip='127.0.0.1', port=8888):
        ##############################################################################
        # TODO:  Connect to the client and get the list of clients it knows          #
        #        Append an entry to self.log                                         #
        ##############################################################################
        correctClient = []
        bootstrapperClients = self.query_bootstrapper_all_clients(curr_time, log=False)
        count = 0
        for client in bootstrapperClients:
            #print("~~~~~len: " + str(len(bootstrapperClients)) + " client: "+str(self.client_id) + " at: "+str(curr_time)+" looking for: "+ str(client_id) + " count: "+ str(count) + " client info: "+str(client[0]) + " " + client[1] + " " + str(client[2]))
            if client[0] == client_id:
                #print("~~~~~client: "+str(self.client_id)+ " found correct client at: "+ str(count) + " " +str(client[0]) + " " + client[1] + " " + str(client[2]))
                correctClient = client
                break
            count += 1

        while self.status == Status.INITIAL:
            pass
        if len(correctClient) > 0:
            otherClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            otherClientSocket.connect((correctClient[1], int(correctClient[2])))
            toSend = str(str(self.client_id) + ' knownClientsPlease '+ '127.0.0.1' +' '+str(self.port))
            # var = struct.pack('i', len(toSend))
            # self.bootstrapperSocket.send(var)
            otherClientSocket.send(toSend.encode('utf-8'))
            #print("     sendList flag sent")
            # length = self.bootstrapperSocket.recv(4)
            # length_hdr = struct.unpack('i', length)[0]
            data = otherClientSocket.recv(1048).decode('utf-8')
            otherClientSocket.close()
            clientDataToList = json.loads(data)
            newData = data.replace('[','<').replace(']','>').replace('\"','')
            newestData = newData[1:len(newData)-1]
            if log:
                q_dict = {}
                q_dict['time'] = curr_time
                q_dict['text'] = "Client " + str(client_id) + ": " + newestData
                print("~~~~~query_client_for_known_client log: "+ "time " + str(curr_time) + " Client " + str(client_id) + ": " + data)
                self.log.append(q_dict)
        return clientDataToList

    def return_list_of_known_clients(self):
        ##############################################################################
        # TODO:  Return the list of clients known to you                             #
        #        HINT: You could make a set of <IP, Port> from self.content_originator_list #
        #        and return it.                                                      #
        ##############################################################################
        
        returnClients = set()
        for content in self.content_originator_list:
            #print("~~~~~return_list_of_known_clients content: "+self.content_originator_list[content][1]+"#"+self.content_originator_list[content][2])
            if self.client_id != int(self.content_originator_list[content][0]):
                returnClients.add((self.content_originator_list[content][0], self.content_originator_list[content][1], self.content_originator_list[content][2]))
        
        returnClients = [list(i) for i in returnClients]
        returnClients = sorted(returnClients, reverse=True)
        if self.client_id == 1:
            return [self.client_id, '127.0.0.1', self.port]
        #print("~~~~~return_list_of_known_clients: "+json.dumps(toReturn))
        return [list(i) for i in returnClients]

    def query_client_for_content_list(self, client_id, curr_time, log = True):
        ##############################################################################
        # TODO:  Connect to the client and get the list of content it has            #
        #        Append an entry to self.log                                         #
        ##############################################################################
        correctClient = []
        if log:
            print("~~~~~~~~~~~query_client_for_content_list called from client_thread")
        bootstrapperClients = self.query_bootstrapper_all_clients(curr_time, log=False)
        count = 0
        for client in bootstrapperClients:
            if client[0] == client_id:
                print("~~~~~client: "+str(self.client_id)+ " found correct client at: "+ str(count) + " " +str(client[0]) + " " + client[1] + " " + str(client[2]))
                correctClient = client
                break
            count += 1

        while self.status == Status.INITIAL:
            pass
        if len(correctClient) > 0:
            otherClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            otherClientSocket.connect((correctClient[1], int(correctClient[2])))
            toSend = str(str(self.client_id) + ' contentList '+ '127.0.0.1' +' '+str(self.port))
            otherClientSocket.send(toSend.encode('utf-8'))
            data = otherClientSocket.recv(1048).decode('utf-8')
            otherClientSocket.close()
            print("~~~~~~~~~~~content list from client: "+str(client_id)+ " "+data)
            clientDataToList = json.loads(data)
            newData = data.replace('[','<').replace(']','>').replace('\"','')
            newestData = newData[1:len(newData)-1]
            if log:
                q_dict = {}
                q_dict['time'] = curr_time
                q_dict['text'] = "Client " + str(client_id) + ": " + newestData
                self.log.append(q_dict)
                print("~~~~~~~~~~~done logging")
            return clientDataToList

    def return_content_list(self):
        ##############################################################################
        # TODO:  Return the content list that you have (self.content)                #
        ##############################################################################
        return self.content.copy()

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
        
        #do we need to keep bootstrapper_all_clients etc from logging? if so how?
        #go though each client and send the content id
        #   each client will check in it's own content for the content ID
        #   if not each clinet will check its COL 
        #   if none of that send a NO
        #   if you get a NO go to next client
        #   if you get a hint then jump to next client
        #   when tou get the data log it an append 
        correctContentClient = ["1","IP","Port"]
        bootstrapperClients = self.query_bootstrapper_all_clients(curr_time, log=False)
        client_index = 0
        hint = 0
        found = False
        loop_count = 0   
        list_of_ids = [i[0] for i in bootstrapperClients]
        print("~~~~~list of ids "+json.dumps(list_of_ids))
        while not found and client_index < len(bootstrapperClients) and loop_count < 10:
            print("~~~~~Client index "+str(client_index) + " " + str(len(bootstrapperClients)))
            client = bootstrapperClients[client_index]
            print("~~~~~Client: "+str(self.client_id)+" Looking at client: "+str(client[0]))
            if client[0] != self.client_id:
                contentList = self.query_client_for_content_list(client[0],curr_time, log=False)
                if not contentList:
                    print("~~~~~content list is empty "+str(client[0]))
                    break
                in_content_list = False
                in_col = None
                for content in contentList:
                    self.content_originator_list[content] = [client[0], client[1], client[2]]
                    if content == content_id:
                        print("~~~~~found content in "+str(client[0]))
                        correctContentClient = [client[0], client[1], client[2]]
                        found = True
                        in_content_list = True
                        break
                if not in_content_list:
                    if content_id in self.content_originator_list:
                        in_col = self.content_originator_list[content_id]
                        hint = in_col[0]
                        print("~~~~~found hint at client_id "+str(hint))
                        client_index = list_of_ids.index(hint)
                    else:
                        client_index += 1
            else:
                client_index += 1
            loop_count += 1


        content_copy = self.content.copy()
        content_copy.append(content_id)
        self.content = content_copy
        print("~~~~~just added new content to client_id: "+str(self.client_id)+ " " + json.dumps(self.content))
        q_dict = {}
        q_dict["time"] = curr_time
        q_dict["text"] = str("Obtained "+str(content_id)+" from " + correctContentClient[1] + "#" + correctContentClient[2])
        self.log.append(q_dict)
       

    def purge_content(self, content_id, curr_time):
        #####################################################################################################
        # TODO:  Delete the content from your content list                                                  #
        #        Append an entry to self.log that content is purged                                         #
        #####################################################################################################

        #still gotta do this
        self.content.remove(content_id)
        purge_dict = {}
        purge_dict["time"] = curr_time
        purge_dict["text"] = str("Removed "+str(content_id))
        self.log.append(purge_dict)
