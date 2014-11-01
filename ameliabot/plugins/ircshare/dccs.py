"""
Author: Iury O. G. Figueiredo.
Name: dccs
Description: It is used to download files that are stored into FOLDER variable path.
It is the counter part of dccg.
Usage:
.dcc_send file_name port

Observation: once the above command is issued the bot running this plugin 
should send a request to send a file to the one who issued the command.

"""

from untwisted.network import *
from untwisted.utils.stdio import CLOSE, CONNECT_ERR
from uxirc.misc import *
from os.path import getsize
from uxirc.dcc import *
from socket import error

HEADER = '\001DCC SEND %s %s %s %s\001' 

class Send(object):
    def __init__(self, server, folder):
        self.folder = folder
        xmap(server, ('PRIVCHAN', '.dcc_send'), self.dcc_send)

    def dcc_send(self, 
                        server, 
                        (
                            nick, user, 
                            host, target, 
                            msg,
                        ),
                        filename,
                        port
                    ):
    
        path = '%s/%s' % (self.folder, filename)

        size = getsize(path)
        fd = open(path, 'rb')
    
        try:
            dccserv = DccServer(fd, int(port))
        except error:
            send_msg(server, nick, "It couldn't listen on the port")
        else:
            request = HEADER % (filename, 
                                ip_to_long(server.myaddr), 
                                port, 
                                size)
        
        
            send_msg(server, nick, request)
        
            def is_done(dccserv, client, msg):
                send_msg(server, nick, msg)
                fd.close()
        
            xmap(dccserv, DONE, is_done, 'Done.')
            xmap(dccserv, CLOSE, lambda dccserv, client, err: is_done(dccserv, client, 'Failed.'))
            xmap(dccserv, ACCEPT_ERR, lambda dccserv, err: is_done(dccserv, None, "Accept error."))
        
            # TIMEOUT is an event that occurs in the dccsev spin
            # instance not in the client instance.
            # The client instance is the spin instance that
            # corresponds to the client socket. So, we need to pass
            # None otherwise we get an exception. The None would correspond
            # to client in the position at is_done.
            xmap(dccserv, TIMEOUT, is_done, None, "TIMEOUT. Server is down.")
        
        

