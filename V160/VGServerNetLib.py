import socket
import threading


# ===========================[C O N S T A N T E S]============================================

BUFFER_SIZE_RECEIVE = 2048



# ===========================[V A R   G L O B A L E S]========================================


# Event list à renvoyer à l'ensemble des player
thLock = threading.Lock()
EventList = []

# Liste des Thread
ThreadList = []


# ========================[ FONCTIONS de GLUES ]===============================================
_lastID = 0
def getNewID():
    """
    Retourne un nouvelle ID (Nécessaire pour l'identification des joueurs)
    """

    global _lastID

    _lastID += 1
    r= _lastID

    return(r)

def AddEvent(cmd):
    """
    Ajoute un évènement dans la liste, utilisé pour les transmettre en block au
    client
    """

    thLock.acquire()
    try:
        EventList.append(cmd)
    finally:
        thLock.release()

    #print("Nb Event in the table:", len(EventList))



# ==========================================================================
# ==     Gestion des messages                                             ==
# ==========================================================================
def SendMessage():


    thLock.acquire()
    try:

        if len(EventList) > 0:
            print("SendMessage:", end='')

            while len(EventList) > 0:
                e = EventList.pop()
                print('[%s].'%(e,), end='')
                for t in ThreadList:
                    print("*", end='')
                    try:
                        t.SendMessage(e)
                    except:
                        pass

            print('$')

    finally:
        thLock.release()


# Classe de gestion d'un client (en Multithreads)
class ClientThread(threading.Thread):

    def __init__(self,ip,port, conn, gfxEngine):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.name=''
        self.Player=None
        self.ID = getNewID()
        self._gfxEngine = gfxEngine

        self.isRunning = False

        print("[+] Un nouveau joueur s'est connecté' d'écoute a été créer pour %s:%d"%(ip,port))

    def run(self):

        self.isRunning = True

        while self.isRunning :

            try:
                data = self.conn.recv(BUFFER_SIZE_RECEIVE)


                if data == b'fin':
                    self.conn.send(b'closing')
                    print("Fermeture du Thread d'écoute")

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # !! Manque la gestion de supression du joueur de la carte
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                    self._gfxEngine.removePlayer(self.Player)
                    self.Player.typePlayer = None
                    self.isRunning = False

                res = self.decode(data)

            except:
                self._gfxEngine.removePlayer(self.Player)
                self.Player.typePlayer = None
                self.isRunning = False


        print("ClientThread: ID=%d [%s] => Arrêt !"%(self.ID, self.name ))

    def stop(self):
        """
        Fonction permettant l'arrêt du Thread
        """
        self.isRunning = False


    def decode(self,data):

        data = data.decode('utf-8')
        data = data.strip()

        k=str(data).split(';')
        for c in k:
            c = c.strip()

            if len(c) == 0:
                continue

            cmd=c.split(":")

            if len(cmd) == 2:

                tCmd = cmd[0].upper()
                tVal = cmd[1]

                print("Commande %s:%s"%(tCmd, tVal))

                if tCmd[0] == 'N':  # Déclaration du Nom du joueur
                    self.name = tVal
                    self.conn.send(bytes(str(self.ID)+':M:'+self.name+'§', 'utf-8'))
                elif tCmd[0] == 'T': # Déclaration du Type du joueur
                    self.setType(tVal)
                    self.SendLog('OK')
                elif tCmd[0] == 'X':  # Déplacement en X
                    self.addX(tVal)
                    self.SendLog('OK')
                elif tCmd[0] == 'Y':  # Déplacement en Y
                    self.addY(tVal)
                    self.SendLog('OK')
                elif tCmd[0] == 'L':  # Récupère les infos sur un joueur ou tous
                    self.getPlayer(tVal)
                elif tCmd[0] == 'C': # Un Joueur en attrappe un autre
                    self.catchPlayer(tVal)

                else:
                    self.SendLog('KO')
                    return(False)
            else:
                self.SendLog('COMMANDE BIDON [%s]'%(c,))
                return(False)

        return(True)



    def getPlayer(self,id):

        global ThreadList

        if id=='*' or id=='' or id==None:
            id=None
        else:
            try:
                id = int(id)
            except:
                return

        #print('>> getPlayer(id=',id,') ::::')
        #print(ThreadList)

        for t in ThreadList:

            #print('>> >> ',t.ID,end='')

            if id == None or (int(id) == int(t.ID)):

                #print('[Trouvé] ',end='')

                if t.Player:
                    msg = '%d:ND:%s:%s:%d:%d:%d'%(t.ID,t.name, t.Player.typePlayer, t.Player.x, t.Player.y, t.Player.score)

                    #print(' => ', msg)
                    self.conn.send(bytes(msg+'§', 'utf-8'))

                if(id == None):
                    continue
                else:
                    return


    def catchPlayer(self,idAttrape):

        p = self._getPlayerFromID(int(idAttrape))

        if(p == None):
            return

        # Le joueur existe => On vérifie que le joueur est bien dans la zone d'attrapage
        if (abs(p.x - self.Player.x) < 2) and (abs(p.y - self.Player.y) < 2):
            print("...Player [%d] attrape [%d] !"%(self.Player.ID, int(idAttrape)))
            self.Player.setPlayerAttrape(int(idAttrape))
            p.setPlayerStatus('A')
            self.Player.isGfxDirty = True # !!!!!
            self._AddEvent('C:%d'%(int(idAttrape)))




    # --------------[ Function haut niveau message Network ]------------------------
    def _AddEvent(self,m):
        """
        Ajoute un message à la file d'attente
        qui sera envoyé à tous les clients
        """
        if (m is None) or (m == ''):
            return

        # Appel de la fonction global
        AddEvent(str(self.ID)+':'+m+'§')


    def _getPlayerFromID(self, ID):

        for t in ThreadList:

            if id == None or (int(ID) == int(t.ID)):
                return(t.Player)

        return(None)



    def SendLog(self, msg):
        """
        Envoie un message de log directement au client
        """

        if(msg is None) or (msg==''):
            return

        msg=">"+msg+'§'
        self.conn.send(bytes(msg, 'utf-8'))

    def SendMessage(self, cmd):
        """
        Envoie un message aux client (une commande)
        """
        if (cmd is None) or (cmd==''):
            return

        self.conn.send(bytes(cmd, 'utf-8'))


    def sendNewPos(self):

        cmd = "POS:"+str(self.Player.x)+':'+str(self.Player.y)
        self._AddEvent(cmd)

    # ---------------------- [ Helper Fonctions ]--------------------------------

    def setType(self,NewType):

        if self.Player:
            if self.Player.typePlayer == NewType:
                print("Déjà instancier du même type")
                return
            else:
                self._gfxEngine.removePlayer(self.Player)
                self.Player.typePlayer = None


        self.Player = self._gfxEngine.addPlayer(NewType)

        if self.Player:
            self._AddEvent('N:'+NewType+':'+str(self.Player.x)+':'+str(self.Player.y))


    def addX(self,val):

            if self.Player == None:
                return
            try:
                v=int(val)
                if self.Player.movePos(v,0):
                    self.sendNewPos()
            except:
                return


    def addY(self,val):

            if self.Player == None:
                return
            try:
                v=int(val)
                if self.Player.movePos(0,v):
                    self.sendNewPos()
            except:
                return


# =============================================================================
# ==                                                                         ==
# ==                             S E R V E U R                               ==
# ==                                                                         ==
# =============================================================================



class ServeurThread(threading.Thread):
    """
    Thread d'écoute et de gestion des nouvelles connexions
    """

    def __init__(self, ecouteIP, ecoutePORT, gfxEngine):
        threading.Thread.__init__(self)

        self._gfxEngine = gfxEngine

        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpServer.bind((ecouteIP, ecoutePORT))
        self.isRunning = False


    def run(self):

        print("ListnerThread: Attente de connexion TCP clientes...")
        global ThreadList
        self.isRunning = True
        self.tcpServer.listen()

        while self.isRunning:

            (conn, (ip,port)) = self.tcpServer.accept()
            newthread = ClientThread(ip,port, conn, self._gfxEngine)
            newthread.start()
            ThreadList.append(newthread)

        # Attend la fin des thread
        for t in ThreadList:
            t.stop()

        self.tcpServer.close()
        print("ListnerThread: Arrêt !")


    def stop(self):
        self.isRunning = False