import random
import time
import sys, signal, os
#import select
import optparse
from socket import *

parser = optparse.OptionParser()
parser.add_option('-p', '--port',     dest="port", default=9000,  type=int  )
parser.add_option('-s', '--server',   dest="server", default="0.0.0.0", )
parser.add_option('-m', '--message',   dest="message",  default="hello", help="messaggio da inviare" )
parser.add_option('-b', '--bufsize',  dest="bufsize", default=1024,  type=int , help="dimensione buffer" )
parser.add_option('-u', '--uri', dest = "uri", default = "/index.html")
parser.add_option('-n', '--name', dest = "name", default = "Cognome")
options, remainder = parser.parse_args()
print ("OPTIONS  server:", options.server, " - port:", options.port, " - bufsize:", options.bufsize)


# Gestione del  ctrl/C
def sigIntHandler(signum, frame): 
    print ("Server exiting ...")
    s.close()
    sys.exit()


print ("   port:", options.port, "  server:", options.server, "bufsize:",options.bufsize)
#creo il socket per lo scambio di pacchetti UDP che conterranno un identificativo della connessione e
#la porta a cui mandare il pacchetto
s = socket(AF_INET,SOCK_DGRAM)
signal.signal(signal.SIGINT, sigIntHandler)
s.bind((options.server,options.port)) #faccio il bind sulla porta di default(9000)

while(1):
        #aspetto il messaggio dal Client
        data,addr = s.recvfrom(options.bufsize)
        print ("addr:",addr," data:", data.decode())

        #genero l'identificativo della connessione
        rand = random.randint(1,1000)
        print("Connessione:" , rand)

        #invio l'identificativo al Client
        Len=s.sendto(str(rand).encode(),addr)
        print ("sent ",Len," Bytes \n")

        #ricevo l'identificativo e la porta in cui inviare il messaggio
        data,addr = s.recvfrom(options.bufsize)
        print ("addr:",addr," data:", data.decode())
        #controllo che l'identificativo sia corretto(Formato messaggio d'arrivo "porta;identificativo")
        if(data.decode().split(";")[1]==str(rand)):
            
            #imposto l'indirizzo: come ip quello da cui ho ricevuto il messaggio e come porta quella che mi è stata mandata nel messaggio
            tcp_addr = (addr[0],int(data.decode().split(";")[0]))
            sock = socket(AF_INET,SOCK_STREAM)
            
            #nel caso il client non sia in ascolto faccio al massimo MAX_TENTATIVI tentativi nel creare la connessione
            #TCP, se tutti falliscono genero un messaggio d'errore
            MAX_TENTATIVI = 5 
            for tentativo in range(MAX_TENTATIVI):
                try:
                    print(f"Tentativo di connessione #{tentativo + 1}...")
                    sock.connect(tcp_addr) 
                    print ("Connesso al server", tcp_addr)
                    break # esci dal ciclo se la connessione riesce
                except ConnectionRefusedError:
                    if tentativo < MAX_TENTATIVI - 1:
                        print("Connessione rifiutata. Attendo 1 secondo prima di riprovare...")
                        time.sleep(1)
                    else:
                        # rilancia l'errore se l'ultimo tentativo fallisce
                        print("Errore nella connessione, client non in ascolto") 
            
            #invio messaggio solo se c'è connessione
            if(tentativo < MAX_TENTATIVI - 1):
                for messaggi in range(5):
                    #invio messaggio con TCP
                    if(messaggi == 4):
                        messaggio="quit"
                    else:
                        messaggio="Messaggio importante " + str(messaggi + 1)

                    print ("Invio: ", messaggio)
                    sock.send(messaggio.encode())

                    risposta = sock.recv(1500).decode()
                    #print (type(risposta))
                    print ("Risposta del client: " , risposta)
            sock.close()


