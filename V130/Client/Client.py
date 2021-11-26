# Python TCP Client A
import socket

host = socket.gethostname()
port = 2021
BUFFER_SIZE = 2000

MegaBuffer = ''

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientA.connect((host, port))


def DecodeMessage():

    global  MegaBuffer

    print("Decode")

    data = ''

    try:
        tcpClientA.setblocking(0)
        data = tcpClientA.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
        print(">>NET => [%s]"%(data,))
    except:
        return

    if data and (len(data) > 0):

        MegaBuffer += data

        p = MegaBuffer.find('§')

        while p >=0 :

            subData = MegaBuffer[0:p]
            MegaBuffer = MegaBuffer[p+1:]

            print(">>Reception de [%s]"%(subData,))
            print(">>Reste ::: [%s]"%(MegaBuffer,))

            if subData == 'closing':
                print('Fermeture du client')
                exit()

            # Cas d'un simple message echo du serveur
            if subData[0] == '>':
                print(subData)
            else:

                # Décomposition du message <idjoueur>:commande:p1:p2

                lParam=subData.split(':')

                print("Réception de ============== [%s] ==========================="%(lParam[0]))
                for i in lParam[1:]:
                    print(i)

            # Boucle while
            p = MegaBuffer.find('§')




msg = ''
while msg.upper()!='FIN':

    #a.upper()[0] != 'O'

    if(msg != ''):
        tcpClientA.send(bytes(msg, 'utf-8'))

    DecodeMessage()
    msg = input('Message:')


tcpClientA.close()