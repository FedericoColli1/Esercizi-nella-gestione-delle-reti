from threading import Thread
from socket import *
import sys, signal
import optparse


parser = optparse.OptionParser()
parser.add_option('-p', '--port',     dest="port", default=9000,  type=int  )
parser.add_option('-s', '--server',   dest="server", default="0.0.0.0", )
parser.add_option('-m', '--message',   dest="message",  default="hello", help="messaggio da inviare" )
parser.add_option('-b', '--bufsize',  dest="bufsize", default=1024,  type=int , help="dimensione buffer" )
parser.add_option('-u', '--uri', dest = "uri", default = "/test.html")
parser.add_option('-n', '--name', dest = "name", default = "Cognome")
options, remainder = parser.parse_args()
print ("OPTIONS  server:", options.server, " - port:", options.port, " - bufsize:", options.bufsize)

# Gestione del  ctrl/C
def sigIntHandler(signum, frame): 
    print ("Server exiting ...")
    s.close()
    sock.close()
    sys.exit()


def ascolto(s,addr):
        risposta = "start"
        while(risposta != "quit"):
            print ("connessione dal Server  ", addr, file = sys.stderr)
            data = s.recv(1500).decode()
            print ('ricevuto ',data, file = sys.stderr)
            answer="successo"
            s.send(answer.encode())
            print ('inviato ' , answer, file = sys.stderr)
            risposta = data
        s.close()



sock = socket(AF_INET, SOCK_STREAM)
#ricerco pagina web del server per verificare correttezza del server
sock.connect((options.server, 80))
#genero il GET
tosend = "GET " + options.uri + " HTTP/1.0\r\n" 
tosend = tosend + "User-Agent: http-client-" + options.name  + "\r\n\r\n"
print (tosend)
sock.send(tosend.encode())

response=sock.recv(options.bufsize).decode()
print (response)

sock.close()
print ("____________________________________________________________________________________")
#dopo aver verificato scambio messaggi UDP per mandare il numero di porta TCP e
#ricevere l'identificativo della connessione
addr = (options.server,options.port)
s = socket(AF_INET,SOCK_DGRAM)
signal.signal(signal.SIGINT, sigIntHandler)

#invio Hello al server per generare la connessione
Len=s.sendto(options.message.encode(),addr) 
print ("sent ",Len," Bytes \n")

#ricevo l'identificativo della connessione 
data,addr = s.recvfrom(options.bufsize)
print ("addr:",addr," data:", data.decode())

#genero il socket TCP
sock = socket(AF_INET, SOCK_STREAM)
#faccio il bind su una porta casuale ed effimera, in cui riceverò il messaggio
sock.bind(('',0))
#prendo il numero di porta dalla combinazione "(0.0.0.0,n_porta)"
n_port = sock.getsockname()[1]
print ('starting up on port ', n_port, file = sys.stderr)

#genero formato messaggio "porta;identificativo"
data_str = data.decode()
info= str(n_port) + ";" + str(data_str)

#invio, tramite sempre UDP, la porta su cui ascolterò
Len=s.sendto(info.encode(),addr)
print ("sent ",Len," Bytes \n")
print ("____________________________________________________________________________________")

#ascolto nella porta effimera
sock.listen(1)
print ('in attesa di una connessione', file = sys.stderr)

#scambio messaggo TCP con il server
s2, c_addr = sock.accept()
#set the thread for the receive request
ric = Thread(target = ascolto, args = (s2,c_addr))
ric.start()
    


s.close()
sock.close()



