from p2pbootstrapper import p2pbootstrapper
import time
import threading

if __name__ == "__main__":
    ##############################################################################
    # You need to perform the following tasks:                                   #  
    # 1) Instantiate the bootstrapper                                            #
    # 2) STart listening on the well-known port                                  #
    # 3) Wait for 5 sec(arbitratry) so that all clients come up and register     #
    # 4) Call bootst.start() which inturn calls the start of all clients       #
    ##############################################################################
    bootst = p2pbootstrapper()
    #print("before start listening")
    listenThread = threading.Thread(target = bootst.start_listening(), args = ())
    listenThread.start()
    #print("after start listening")
    time.sleep(5)
    #print("call bootstrapper start")
    bootst.start()
    ##############################################################################
    #  We know that listenign on a port is a blocking action, and the B.S        #
    #  cannot call start() once it starts listening. Threads to the rescue!     #
    #                                    e                                        #
    #  For step 2) create a thread to handl bootst.start_listening() method     #
    #  Now execute steps 3 and 4.                                                #
    ##############################################################################    
