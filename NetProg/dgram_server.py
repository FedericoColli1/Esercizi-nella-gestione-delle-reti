
import sys, signal, os
#import select
import optparse
from socket import *

parser = optparse.OptionParser()
parser.add_option('-p', '--port',     dest="port", default=9000,  type=int  )
parser.add_option('-s', '--server',   dest="server", default="0.0.0.0", )
parser.add_option('-b', '--bufsize',  dest="bufsize", default=1024,  type=int , help="dimensione buffer" )
options, remainder = parser.parse_args()


# Gestione del  ctrl/C
def sigIntHandler(signum, frame): 
    print ("Server exiting ...")
    s.close()
    sys.exit()


print ("   port:", options.port, "  server:", options.server, "bufsize:",options.bufsize)

s = socket(AF_INET,SOCK_DGRAM)
signal.signal(signal.SIGINT, sigIntHandler)
s.bind((options.server,options.port))

while(1):
        data,addr = s.recvfrom(options.bufsize)
        print ("addr:",addr," data:", data.decode())

