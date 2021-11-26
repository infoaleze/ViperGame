import socket



# Buffeur de données reçu par le Réseau
# pour le décodage des message
MegaBuffer = ''

# Paramètre par défaut 
port = 2021
BUFFER_SIZE = 2000
MegaBuffer = ''


# Création de l'objet Réseau
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def Connect(ServeurName):
    '''
    Fonction de connexion au serveur
    '''

    try:
        tcpClientA.connect((ServeurName, port))
    except:
        print("[!] Erreur de connexion")


def Send(msg):

    tcpClientA.send(bytes(msg+';', 'utf-8'))


# ========================================================================
# ==                                                                    ==
# ==        Fonctions liés aux traitements des messages                 ==
# ==                                                                    ==
# ========================================================================

def DecodeMessage():

    '''
    Cette fonction assure la lecture du buffeur réçu au niveau du réseau
    et du décodage des messages

    3 cas:

    'closing' : 
        Indique au client de l'arrêt du serveur
    commence par '>' :                     
        C'est un message à afficher, pour l'instant est traduit par un print
    <idJoueur>:<Fonction>[[:<Param1>]..] : 
        Instruction avec 0 ou n paramètre(s) relatif au joueur <IdJoueur>

    La fonction retourne une liste de message :
    [
        {id:<IdJoueur>, inst:<Fonction>, param:[ 'p1', ... ]},
        { ... }
    ]


    retorune:
    -1   : => Message de fermeture
    <str>: => Message à afficher
    []   : => Tableau d'instruction, peu ne rien contenir

    '''

    global  MegaBuffer

    #print(">> DecodeMessage")

    data = ''


    # Tentative de lecture d'un nouveau block de message
    try:
        tcpClientA.setblocking(0)
        data = tcpClientA.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
        #print(".. Reception NET => [%s]"%(data,))

        if data and (len(data) > 0):
            MegaBuffer += data

    except:
        pass


    # Boucle de décodage
    p = MegaBuffer.find('§')

    listMsg = []

    while p >=0 :

        subData = MegaBuffer[0:p]
        

        #print(".. Reception de [%s]"%(subData,))
        #print(".. Reste ::: [%s]"%(MegaBuffer,))

        if subData == 'closing':
            print('Fermeture du client')
            return(-1)

        # Cas d'un simple message echo du serveur
        if subData[0] == '>':
            #print(subData)

            # Si il y a des donnée déjà décoder, on envoie, en laissant le message
            if len(listMsg) > 0:
                return listMsg

            # On retire le message et on le retourne
            MegaBuffer = MegaBuffer[p+1:]
            return(subData[1:])
        else:

            MegaBuffer = MegaBuffer[p+1:]

            # Décomposition du message <idjoueur>:commande:p1:p2            
            lParam=subData.split(':')

            #print("Réception de ============== [%s] ==========================="%(lParam[0]))
            #for i in lParam[1:]:
            #    print(i)

            listMsg.append( { 'id':int(lParam[0]), 'inst':lParam[1], 'params': lParam[2:]} )

        # Boucle while
        p = MegaBuffer.find('§')


        return(listMsg)
