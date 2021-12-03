import pygame


# Librairie de décodage des message
import VGLib



# constantes

COUL_VERT  = (0, 255, 0)
COUL_ROUGE = (255, 0, 0)
COUL_BLEU  = (0, 0, 255)
COUL_GRIS  = (73, 73, 73)
COUL_NOIR  = (0, 0, 0)

COUL_POULE = (0xFF, 0xE4, 0x36)
COUL_RENARD = (0x7e, 0x58, 0x35)
COUL_VIPER = (95, 138, 7)


# ===== Variables Globales =========================================
LName = 'TOTO'
LType = 'P'
LID = 0

# ==================================================================
# ==                INITIALISATION DE PYGAME                      ==
# ==================================================================

# configuration de Base pour le moteur pyGame
pygame.init()
fenetre = pygame.display.set_mode((750, 750))
pygame.display.set_caption("The Viper Game Client")


# G R O U P E   D E  S p R i T e S
playerGroupe = pygame.sprite.Group()


# ==================================================================
# ==             O B J E T S   G R A P H I Q U E S                ==
# ==================================================================

class VPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.typePlayer = None
        self.score = 0

        self.setImage()

    def setImage(self):

        if self.typePlayer == 'P':
            self.image = pygame.image.load("./images/Poule.png")            
        elif self.typePlayer == 'R':
            self.image = pygame.image.load("./images/Renard.png")
        elif self.typePlayer == 'V':
            self.image = pygame.image.load("./images/Viper.png")
        else:
            self.image = pygame.Surface([25,25])
            self.image.fill(COUL_GRIS)

        self.rect = self.image.get_rect()  # rectangle de colision

    def setTypePlayer(self,TPlayer):

        self.typePlayer = TPlayer
        self.setImage()

    def draw(self):
        fenetre.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        pass



class VLocalPlayer(VPlayer):

    def __init__(self):
        VPlayer.__init__(self)

    def setImage(self):
        
        if self.typePlayer == 'P':
            self.image = pygame.image.load("./images/PouleL.png")            
        elif self.typePlayer == 'R':
            self.image = pygame.image.load("./images/RenardL.png")
        elif self.typePlayer == 'V':
            self.image = pygame.image.load("./images/ViperL.png")
        else:
            self.image = pygame.Surface([25,25])
            self.image.fill(COUL_GRIS)

        self.rect = self.image.get_rect()  # rectangle de colision



# =====================[ Fonctions GUI ]============================

def UpdatePOS(player, X, Y):

    if player == None:
        return

    player.rect.x = X
    player.rect.y = Y
    

# ==================================================================
# ==                                                              ==
# ==            F O N C T I O N S   D ' A I D E                   ==
# ==                                                              ==
# ==================================================================

def CheckPalyerList(pID, pParam):

    global playerGroupe, LID

    # pParam = <Name>:<Type>:<X>:<Y>:<Score>

    # Recherche si le joueur existe déjà
    for k in playerGroupe:

        
        if k.ID==pID:
            # Le joueur est trouvé
            # alors mis à jour
            k.name = pParam[0]
            k.setTypePlayer(pParam[1])
            k.rect.x = int(pParam[2])
            k.rect.y = int(pParam[3])
            return

    # Fin de boucle => pas trouvé
    # => Ajout

    # Est un nouveau joueur ou moi même
    if pID == LID:
        # C'est moi
        print("C'est moi ! %d,%d"%(pID,LID))
        NPlayer =  VLocalPlayer()
    else:
        # Ce n'est pas moi
        NPlayer =  VPlayer()

    
    NPlayer.ID = pID
    NPlayer.name = pParam[0]
    NPlayer.setTypePlayer(pParam[1])
    NPlayer.rect.x = int(pParam[2])
    NPlayer.rect.y = int(pParam[3])

    playerGroupe.add(NPlayer)


# Recherche un joueur dans la liste
def FindPlayer(pID):

    for p in playerGroupe:

        if(p.ID == pID):
            return(p)
    
    return(None)





# ==================================================================
# ==        G E S T I O N   D E S    M E S S A G E S              ==
# ==================================================================
def ReceptionMessage():

    global run, LID, LType


    ret = VGLib.DecodeMessage()

    if type(ret) == list:

        # Message a traiter
        if len(ret) > 0:
            for m in ret:
                print("Msg de [%6d] : [%10s] : %s"%(m['id'],m['inst'],m['params']))

                if m['inst'] == 'M':
                    print("[i] Joueur inscrit avec l'ID %d"%(m['id'],))
                    LID = m['id']
                    # Envoie de la commande du Type choisi
                    VGLib.Send('T:'+LType)

                if m['inst'] == 'ND':
                    # Mise à jour de la liste des joueurs
                    CheckPalyerList(m['id'],m['params'] )

                if m['inst'] == 'N':
                    # Récupère le pédigré du joueur
                    VGLib.Send('L:'+str(m['id']))

                if m['inst'] == 'POS':
                    p = FindPlayer(m['id'])
                    UpdatePOS(p,int(m['params'][0]), int(m['params'][1]))

        return

    # Affichage des messages
    if type(ret) == str:
        print("MSG> ", ret)

    elif ret == -1:
        run = False


# ==================================================================
# ==        E N V O I E   D e s   E V E N E M E N T S             ==
# ==================================================================  

def UpdatePos(Dir, Nb):

    if Dir=='H':
        VGLib.Send('Y:'+str(-Nb))
    elif Dir == 'B':
        VGLib.Send('Y:'+str(Nb))
    elif Dir == 'G':
        VGLib.Send('X:'+str(-Nb))           
    elif Dir == 'D':
        VGLib.Send('X:'+str(Nb))        






# ==================================================================
# ==   G E S T I O N   D E S   O B J E T S   G R A P H I Q U E S  ==
# ==================================================================
def Redessine():

    fenetre.fill(COUL_NOIR)

    # Titre
    font = pygame.font.SysFont("Consolas", 30)
    text = font.render("V1p3r G@m3 Client", False, COUL_VERT)
    textRect = text.get_rect()
    textRect.center = (750 // 2, 25)
    fenetre.blit(text, textRect)


    # Dessine les joueurs
    playerGroupe.update()
    playerGroupe.draw(fenetre)


    pygame.display.update()
    



# ==================================================================
# ==                INITIALISATION Du RESEAU                      ==
# ==================================================================


VGLib.Connect('localhost')


# Inscription du joueur
VGLib.Send('N:'+LName)

# Récupération des joueurs déja présent
VGLib.Send('L:')
ReceptionMessage()


# ==========================================================================
# ==               B O U C L E   P R I N C I P A L E
# ==========================================================================

run = True

while run:
    pygame.time.delay(20)


    ReceptionMessage()

    Redessine()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            UpdatePos('G',10)
        if key[pygame.K_RIGHT]:
            UpdatePos('D',10)           
        if key[pygame.K_UP]:
            UpdatePos('H',10)
        if key[pygame.K_DOWN]:
            UpdatePos('B',10)           




pygame.quit()

