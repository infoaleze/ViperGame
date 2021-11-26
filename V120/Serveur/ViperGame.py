import pygame
import random

import socket
import threading


# constantes

COUL_VERT  = (0, 255, 0)
COUL_ROUGE = (255, 0, 0)
COUL_BLEU  = (0, 0, 255)
COUL_NOIR  = (0, 0, 0)


# configuration de Base pour le moteur pyGame
pygame.init()
fenetre = pygame.display.set_mode((750, 750))
pygame.display.set_caption("The Viper Game Serveur")

# V110

_lastID = 0
def getNewID():

    global _lastID

    _lastID += 1
    r= _lastID

    return(r)



# ==========================================================================
# ==                  C L A S S E   D E S   S P R I T E S
# ==========================================================================

class ViperPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25,25])
        #self.image = pygame.image.load("Alien.png")
        self.image.fill(COUL_VERT)
        self.rect = self.image.get_rect()  # rectangle de colision
        self.typePlayer = 'V'
        self.score = 0

    def draw(self):
        fenetre.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        pass


class PoulePlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25,25])
        #self.image = pygame.image.load("Alien.png")
        self.image.fill(COUL_BLEU)
        self.rect = self.image.get_rect()  # rectangle de colision
        self.typePlayer = 'P'
        self.score = 0

    def draw(self):
        fenetre.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        pass

class RenardPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25,25])
        #self.image = pygame.image.load("Alien.png")
        self.image.fill(COUL_ROUGE)
        self.rect = self.image.get_rect()  # rectangle de colision
        self.typePlayer = 'R'
        self.score = 0

    def draw(self):
        fenetre.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        pass

# ==========================================================================
# ==                  G R O U P E   D E  S p R i T e S
# ==========================================================================
viperGroupe = pygame.sprite.Group()
pouleGroupe = pygame.sprite.Group()
renardGroupe= pygame.sprite.Group()

# ==========================================================================
# ==                 G l U e C o D e   R é S e A u x
# ==========================================================================

BUFFER_SIZE_RECEIVE = 2048
TCP_IP = '0.0.0.0'
TCP_PORT = 2021

# Event list à renvoyer à l'ensemble des player
thLock = threading.Lock()
EventList = []
ThreadList = []

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
                print('.', end='')
                for t in ThreadList:
                    print("*", end='')
                    try:
                        t.SendMessage(e)
                    except:
                        pass

            print('$')

    finally:
        thLock.release()

def AddEvent(cmd):

    thLock.acquire()
    try:
        EventList.append(cmd)
    finally:
        thLock.release()

    print("Nb Event in the table:", len(EventList))







# Protocole

# <cmd1>[;<cmd2>...]

# N:<Name>, T: { V | P | R }
# X:<+/->Val
# Y:<+/->Val

# Classe de gestion d'un client (en Multithreads)
class ClientThread(threading.Thread):

    def __init__(self,ip,port, conn):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.name=''
        self.typePlayer=None
        self.ID = getNewID()
        print("[+] Un nouveau joueur s'est connecté' d'écoute a été créer pour %s:%d"%(ip,port))

    def run(self):
        while True :
            data = self.conn.recv(BUFFER_SIZE_RECEIVE)


            if data == b'fin':
                self.conn.send(b'closing')
                print("Fermeture du Thread d'écoute")
                break

            res = self.decode(data)


    def decode(self,data):

        data = data.decode('utf-8')
        data = data.strip()

        k=str(data).split(';')
        for c in k:
            c = c.strip()
            cmd=c.split(":")

            if len(cmd) == 2:

                tCmd = cmd[0].upper()
                tVal = cmd[1]

                print("Commande %s:%s"%(tCmd, tVal))

                if tCmd[0] == 'N':
                    print(str(self.ID)+'N')
                    self.name = tVal
                    self.conn.send(bytes('M:'+str(self.ID)+':'+self.name+'§', 'utf-8'))
                elif tCmd[0] == 'T':
                    print(str(threading.get_ident())+'T='+tVal)
                    self.setType(tVal)
                    self.conn.send(bytes('>OK§', 'utf-8'))
                elif tCmd[0] == 'X':
                    print(str(threading.get_ident())+'X')
                    self.addX(tVal)
                    self.conn.send(bytes('>OK§', 'utf-8'))
                elif tCmd[0] == 'Y':
                    print(str(threading.get_ident())+'Y')
                    self.addY(tVal)
                    self.conn.send(bytes('>OK§', 'utf-8'))
                elif tCmd[0] == 'L':
                    self.getPlayer(tVal)

                else:
                    self.conn.send(bytes('>KO§', 'utf-8'))
                    return(False)
            else:
                self.conn.send(bytes('>COMMANDE BIDON', 'utf-8'))
                return(False)

        return(True)



    def getPlayer(self,id):

        global ThreadList

        if id=='' or id==None: 
            id=None
        else:
            try:
                id = int(id)
            except:
                return

        print('>> getPlayer(id=',id,') ::::')
        print(ThreadList)

        for t in ThreadList:

            print('>> >> ',t.ID,end='')

            if id == None or (int(id) == int(t.ID)): 

                print('[Trouvé] ',end='')

                if t.typePlayer:
                    msg = '%d:ND:%s:%s:%d:%d:%d'%(t.ID,t.name, t.typePlayer.typePlayer, t.typePlayer.rect.x, t.typePlayer.rect.y, t.typePlayer.score)

                    print(' => ', msg)
                    self.conn.send(bytes(msg+'§', 'utf-8'))

                if(id == None):
                    continue
                else:
                    return



    def SendMessage(self, cmd):

        if (cmd is None) or (cmd==''):
            return

        print("<<Th:"+cmd+">>")

        self.conn.send(bytes(cmd, 'utf-8'))

    def sendNewPos(self):

        cmd = "POS:"+str(self.typePlayer.rect.x)+':'+str(self.typePlayer.rect.y)
        self._AddEvent(cmd)
        

    def _AddEvent(self,m):

        if (m is None) or (m == ''):
            return

        # Appel de la fonction global
        AddEvent(str(self.ID)+':'+m+'§')



    def setType(self,NewType):

        if self.typePlayer:
            if self.typePlayer.typePlayer == NewType:
                print("Déjà instancier du même type")
                return
            else:
                if self.typePlayer.typePlayer == 'V':
                    viperGroupe.remove(self.typePlayer)
                elif self.typePlayer.typePlayer == 'R':
                    renardGroupe.remove(self.typePlayer)
                elif self.typePlayer.typePlayer == 'P':
                    pouleGroupe.remove(self.typePlayer)

                self.typePlayer.typePlayer = None


        if NewType == 'V':
            self.typePlayer =  ViperPlayer()
            self.typePlayer.rect.x = random.randrange(50,700)
            self.typePlayer.rect.y = random.randrange(50,700)
            viperGroupe.add(self.typePlayer)
            self._AddEvent('N:V:'+str(self.typePlayer.rect.x)+':'+str(self.typePlayer.rect.y))
            print("Ajout Viper")

        elif NewType == 'P':
            self.typePlayer =  PoulePlayer()
            self.typePlayer.rect.x = random.randrange(50,700)
            self.typePlayer.rect.y = random.randrange(50,700)
            pouleGroupe.add(self.typePlayer)
            self._AddEvent('N:P:'+str(self.typePlayer.rect.x)+':'+str(self.typePlayer.rect.y))
            print("Ajout Poule")


        elif NewType == 'R':
            self.typePlayer =  RenardPlayer()
            self.typePlayer.rect.x = random.randrange(50,700)
            self.typePlayer.rect.y = random.randrange(50,700)
            renardGroupe.add(self.typePlayer)
            self._AddEvent('N:R:'+str(self.typePlayer.rect.x)+':'+str(self.typePlayer.rect.y))
            print("Ajout Renard")

        print('Nb Poule=%d, Viper=%d, Renard=%d.'%(len(pouleGroupe),len(viperGroupe),len(renardGroupe) ))

    def addX(self,val):

            if self.typePlayer == None:
                return
            try:
                v=int(val)
                if(v > -50) and (v < 50):
                    if (self.typePlayer.rect.x + v < 750) and (self.typePlayer.rect.x + v > 0):
                        self.typePlayer.rect.x += v
                        self.sendNewPos()
            except:
                return


    def addY(self,val):

            if self.typePlayer == None:
                return
            try:
                v=int(val)
                if(v > -50) and (v < 50):
                    if (self.typePlayer.rect.y + v < 750) and (self.typePlayer.rect.y + v > 0):
                        self.typePlayer.rect.y += v
                        self.sendNewPos()
            except:
                return

# Classe Reseau Serveur d'écoute
class ListnerThread(threading.Thread):

    def __init__(self, ecouteIP, ecoutePORT):
        threading.Thread.__init__(self)
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpServer.bind((ecouteIP, ecoutePORT))


    def run(self):

        print("ListnerThread: Attente de connexion TCP clientes...")
        global ThreadList


        while True:

            self.tcpServer.listen()
            (conn, (ip,port)) = self.tcpServer.accept()
            newthread = ClientThread(ip,port, conn)
            newthread.start()
            ThreadList.append(newthread)

        # Attend la fin des thread
        for t in ThreadList:
            t.join()


# Démarrage du Serveur
ServerThread = ListnerThread(TCP_IP, TCP_PORT)
ServerThread.start()





# ==========================================================================
# ==                  R E D E S S I N E
# ==========================================================================
def Redessine():

    fenetre.fill(COUL_NOIR)

    # Titre
    font = pygame.font.SysFont("Consolas", 30)
    text = font.render("V1p3r G@m3", False, COUL_ROUGE)
    textRect = text.get_rect()
    textRect.center = (750 // 2, 25)
    fenetre.blit(text, textRect)

    # Dessine les joueurs
    viperGroupe.update()
    viperGroupe.draw(fenetre)

    pouleGroupe.update()
    pouleGroupe.draw(fenetre)

    renardGroupe.update()
    renardGroupe.draw(fenetre)

    pygame.display.update()





# ==========================================================================
# ==               B O U C L E   P R I N C I P A L E
# ==========================================================================

run = True

while run:
    pygame.time.delay(100)


    SendMessage()

    Redessine()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False




pygame.quit()
