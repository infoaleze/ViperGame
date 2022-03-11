from lib2to3.pgen2.token import LPAR
from sys import api_version
import pygame

import VGCore


LVGNetLib = None

# ==================================================================
# ==               DEFINITION DES CONSTANTES                      ==
# ==================================================================

COUL_VERT  = (0, 255, 0)
COUL_ROUGE = (255, 0, 0)
COUL_BLEU  = (0, 0, 255)
COUL_GRIS  = (73, 73, 73)
COUL_NOIR  = (0, 0, 0)

COUL_POULE  = (0xFF, 0xE4, 0x36)
COUL_RENARD = (0x7e, 0x58, 0x35)
COUL_VIPER  = (95,   138,  7)

# ==================================================================
# ==                INITIALISATION DE PYGAME                      ==
# ==================================================================

# configuration de Base pour le moteur pyGame
pygame.init()


# ==================================================================
# ==                DEFINTION DES CLASSES ECRAN                   ==
# ==================================================================

class GfxScreen:
    def __init__(self, Titre, baseDir):

        # Définition des propriétés
        self.rx = 25    # Taille en X du sprite
        self.ry = 25    # Taille en Y du sprite

        self._baseDir = baseDir

        self.fenetre = pygame.display.set_mode((self.sx, self.sy))
        pygame.display.set_caption(Titre)

        self.photo_back = None  # Image de fond

        self.fen_plateau = None # Espace graphique du jeu
        self.fen_header  = None # Espace graphique du titre/score
        self.fen_msg     = None # Espace graphique des messages
        self.fen_prop    = None # Espace des infos/propriétés du jeu

        self.pox = 0    # Offset en X de la map par rapport à l'espace graphique de la fen_plateau
        self.poy = 0    # Offset en Y de la map par rapport à l'espace graphique de la fen_plateau

        # Initialisation des espaces graphiques
        self.initGfxSpace()

    def getScreenSize(self):
        # Taille par défaut
        return (750,750)

    def getPlateauSize(self):
        # Taille par défaut
        return (30,30)

    def drawBackground(self, Theme=None):

        self.fenetre.fill(COUL_NOIR)

        if self.photo_back is not None:

            (bw,bh) = self.photo_back.get_size()

            if bw > self.sx:
                oX = self.sx - bw
            else:
                oX = bw - self.sx

            if bh > self.sy:
                oY = self.sy - bh
            else:
                oY = bh - self.sy

            self.fenetre.blit(self.photo_back, ( oX // 2, oY//2))

    def initGfxSpace(self):

        pass


    def Update(self):

        pygame.time.delay(20)

        return(True)


class GfxScreenFHD(GfxScreen):

    def __init__(self, Titre, baseDir='.'):

        self.sx = 1920 # taille de l'écran global
        self.sy = 1080
        self.pcx = 59 # Taille en case du plateau
        self.pcy = 35

        # appel du constructeur hérité
        GfxScreen.__init__(self, Titre, baseDir)

    def drawBackground(self, Theme=None):

        if Theme is not None:
            self.photo_back = pygame.image.load(self._baseDir+"/images/"+ Theme +"/background_FHD.png")

        else:
            self.photo_back = None

        GfxScreen.drawBackground(self, Theme)

    def initGfxSpace(self):

        self.fen_plateau = self.fenetre.subsurface( pygame.rect.Rect(416,68,1488,896) )
        self.fen_header  = None # Espace graphique du titre/score
        self.fen_msg     = None # Espace graphique des messages
        self.fen_prop    = None # Espace des infos/propriétés du jeu



class GfxScreenHD(GfxScreen):

    def __init__(self, Titre, baseDir):

        self.sx = 1366 # taille de l'écran global
        self.sy = 768
        self.pcx = 31 # Taille en case du plateau
        self.pcy = 19

        # appel du constructeur hérité
        GfxScreen.__init__(self, Titre, baseDir)



# ==================================================================
# ==            DEFINTION DES CLASSES DES JOUEURS                 ==
# ==================================================================

class GfxPlayer(VGCore.VPlayer):

    """
    Cette classe dérive de la classe VPlayer afin de définir
    les méthodes et propriété pour l'affichage d'un joueur
    en mode graphique
    """

    def __init__(self):
        """
        Fonction d'initilisation:
        """
        # appel du constructeur hérité
        VGCore.VPlayer.__init__(self)
        self.image = None
        self.isGfxDirty = True
        self.setImage()

    def setTypePlayer(self, TPlayer):

        VGCore.VPlayer.setTypePlayer(self, TPlayer)
        self.isGfxDirty = True
        self.setImage()


    def setImage(self):
        """
        Fonction assurant le chargement du sprite correspondant
        en fonction du type de joueur, et si il est local ou pas
        """

        if self._isLocal:

            if self.typePlayer == 'P':
                if self.playerState == 'C':
                    self.image = pygame.image.load("./images/PouleLA.png")
                else:
                    self.image = pygame.image.load("./images/PouleL.png")
            elif self.typePlayer == 'R':
                if self.playerState == 'C':
                    self.image = pygame.image.load("./images/RenardLA.png")
                else:
                    self.image = pygame.image.load("./images/RenardL.png")
            elif self.typePlayer == 'V':
                if self.playerState == 'C':
                    self.image = pygame.image.load("./images/ViperLA.png")
                else:
                    self.image = pygame.image.load("./images/ViperL.png")
            else:
                self.image = pygame.Surface([25,25])
                self.image.fill(COUL_GRIS)

        else:

            if self.typePlayer == 'P':
                if self.playerState == 'C':
                    self.image = pygame.image.load("./images/PouleA.png")
                else:
                    self.image = pygame.image.load("./images/Poule.png")
            elif self.typePlayer == 'R':
                if self.playerState == 'C':
                    self.image = pygame.image.load("./images/RenardA.png")
                else:
                    self.image = pygame.image.load("./images/Renard.png")
            elif self.typePlayer == 'V':
                if self.playerState == 'C':
                    self.image = pygame.image.load("./images/ViperA.png")
                else:
                    self.image = pygame.image.load("./images/Viper.png")
            else:
                self.image = pygame.Surface([25,25])
                self.image.fill(COUL_GRIS)

        self.isGfxDirty = False


    def Draw(self,myScreen, myMap):
        """
        Fonction qui dessine le joueur à dans le context graphique
        passé en paramètre.
        """

        # Vérifie que le player n'est pas dans un état invisible
        # ??????????????
        # ??????????????
        # ??????????????
        # ??????????????

        if myMap.isVisible(self.x, self.y):

            px = myScreen.pox + (self.x - myMap.oX) * myScreen.rx
            py = myScreen.poy + (self.y - myMap.oY) * myScreen.ry

            myScreen.fen_plateau.blit(self.image, (px, py))


# ==================================================================
# ==        CLASSE ASSURANT LE DESSIN DE LA CARTE                 ==
# ==================================================================

class GfxMap():

    def __init__(self, Map):

        # Initialisation des propriétés
        self.photo_wall_list = []   # Images des murs
        self.photo_camp_list = []   # Images des camps

        self.gfxPlateau = None # Image précalculé du plateau de jeu
        self.lastTheme = None


        self._Map = Map         # Référence sur l'objet VMap
        self._Screen = None     # Référence sur l'objet Context Graphique
                                # Sera affecté au moment de l'assoication entre
                                # la Map et le context graphique


        self.oX = 0             # Offset en X
        self.oY = 0             # Offset en Y (unité Case)


    def reInit(self):
        """
        Fonction utilisée lors d'un changement de carte
        """

        self.gfxPlateau = None # Image précalculée du plateau de jeu

        # Rechargement des ressources graphiques si thème différent
        self._initGfx()



    def _initGfx(self):
        """
        Charge les ressources graphiques
        """

        if (self.lastTheme is None) or (self.lastTheme !=  self._Map.Theme):

            # Vide les listes actuelles
            self.photo_wall_list.clear()
            self.photo_camp_list.clear()

            # Extraction des images mur
            self.sprite_wall = pygame.image.load(self._Screen._baseDir + "/images/"+self._Map.Theme +"/walls.png").convert_alpha()

            for i in range(0,1) :
                    rect = pygame.Rect(i*self._Screen.rx,0,self._Screen.rx,self._Screen.rx)
                    img = self.sprite_wall.subsurface(rect)
                    #img.load()
                    self.photo_wall_list.append(img)

            # Extraction des images camp
            self.sprite_camp = pygame.image.load(self._Screen._baseDir + "/images/"+self._Map.Theme +"/camps.png").convert_alpha()
            for i in range(0,3) :
                    rect = pygame.Rect(i*self._Screen.rx,0,self._Screen.rx,self._Screen.rx)
                    img = self.sprite_camp.subsurface(rect)
                    #img.load()
                    self.photo_camp_list.append(img)

            self.lastTheme = self._Map.Theme


    def GenerePlateau(self):
        """
        Cette fonction s'occupe de dessiner le plateau (mur et camp)
        """

        # Définition de la taille du plateau

        self.gfxPlateau = pygame.Surface((self._Map.LX * self._Screen.rx, self._Map.LY * self._Screen.ry)).convert_alpha()


        # Génération des murs

        # Pour chaque ligne du plateau
        for ly in range(0,self._Map.LY):

            # Pour chaque colone du plateau
            for lx in range(0,self._Map.LX):
                code = self._Map.Carte[ly * self._Map.LX + lx]

                #Est un mur ?
                if (code & 0xFF) == 0xFF:
                    self.gfxPlateau.blit(self.photo_wall_list[0],(lx*self._Screen.rx, ly*self._Screen.ry))

                #Est un camp ?
                elif ((code & 0x03) > 0):
                    # C'est un camp
                    self.gfxPlateau.blit(self.photo_camp_list[(code & 0x03) - 1],(lx*self._Screen.rx, ly*self._Screen.ry))


    def DessineTout(self, pX=0, pY=0):
        """
        Cette fonction assure la génération du plateau de jeu
        Plus le calcul de l'offset pour affichage en fonction
        de la taille de l'espace plateau et de la position du
        joueur


        Met à jour:
            self.oX, self.oY : offset logique (ox,oy) : unité = case logique
            _Screen.pox, _Screen.poy offset cadre affichage (cX,cY) : unité = pixel

        """

        if self.gfxPlateau is None:
            self.GenerePlateau()


        # Taille de la carte
        mLX = self._Map.LX
        mLY = self._Map.LY


        # Check des bornes
        if (pX < 0): pX = 0
        if (pY < 0): pY = 0

        if (pX > mLX): pX = mLX-1
        if (pY < mLY): pY = mLY-1


        # Calcul la portion du plateau à copier en fonction de la taille
        # d'affichage et de la position du joueur principal (local)

        # Taille de l'affichage disponnible
        pcX = self._Screen.pcx
        pcY = self._Screen.pcy

        # Taille de la carte
        mLX = self._Map.LX
        mLY = self._Map.LY

        # Calcul des Offset (Décalages):
        # oX, oY = Décalage en case de la portion de la Carte à afficher
        # cX, cY = Décalage en cas de centrage en pixel (cas de carte plus petite)
        if(pcX >= mLX):
            self.oX = 0
            cX = (pcX-mLX) * self._Screen.rx // 2
        else:
            cX = 0
            if pX < (pcX // 2):
                self.oX = 0
            else:
                self.oX = pX - (pcX // 2)

        if(pcY >= mLY):
            self.oY = 0
            cY = (pcY-mLY) * self._Screen.ry // 2
        else:
            cY = 0
            if pY < (pcY // 2):
                self.oY = 0
            else:
                self.oY = pY - (pcY // 2)


        self._Screen.pox = cX
        self._Screen.poy = cY

        # Dessine la partie de la map Visible dans la fenêtre final
        self._Screen.fen_plateau.blit(self.gfxPlateau,
                    ((cX-self.oX*self._Screen.rx), (cY-self.oY*self._Screen.ry)))


    def isVisible(self,x,y):
        """
        Cette fonction s'occupe de calculer si un élément est visible
        dans la partie de la carte affiché ou pas
        """

        minX = max (0, self.oX)
        minY = max (0, self.oY)
        maxX = min (self._Map.LX, self.oX+self._Screen.pcx)
        maxY = min (self._Map.LY, self.oY+self._Screen.pcy)


        if (x<minX) or (y<minY) or (x>maxX) or (y > maxY) :
            return False

        return True



# ==================================================================
# ==        DEFINTION DE LA CLASSES MOTEUR GRAPHQIUE              ==
# ==================================================================
class GfxEngine():

    def __init__(self, myScreen, myGfxMap):
        """
        Fonction d'initilisation:
        """

        self._Screen  = myScreen
        self._Map     = myGfxMap

        if self._Map is not None:
            self._Map._Screen = myScreen
            # Initialise les ressource Graphique de la Map
            self._Map.reInit()

        self.bgHasChanged = True   # Provoquera le chargement de l'image de fond

        # Liste des joueur
        self.playerList = VGCore.EntityList(myGfxMap)


        # LocalPlayer Data
        self.LPName = ''
        self.LPType = ''


    def initialise(self, Pname, Ptype):

        # Envoie la commande de déclaration

        self.LPName = Pname
        self.LPType = Ptype

        # Déclaration du nouveau joueurs
        LVGNetLib.Send('N:'+Pname)
        # Récupère la liste des joueurs
        LVGNetLib.Send('L:')
        self.receptionMessage()



    # ============================ [ Helper Fonctions ]==============================
    def checkPlayerList(self, pID, pParam):

        p = self.playerList.getPlayer(pID)

        if(p):
            p.name = pParam[0]
            p.setTypePlayer(pParam[1])
            p.moveTo( int(pParam[2]), int(pParam[3]) )
            return

        # => pas trouvé
        # => Ajout

        if pID == self.playerList.LocalPlayerID:
            # C'est moi
            NPlayer = GfxPlayer()
            NPlayer.ID = pID
            NPlayer.setIsLocal(True)
            self.playerList.addLocalPlayer(NPlayer)
        else:
            # Ce n'est pas moi
            NPlayer = GfxPlayer()
            NPlayer.ID = pID
            NPlayer.setIsLocal(False)
            self.playerList.addPlayer(NPlayer)

        NPlayer.setTypePlayer(pParam[1])
        NPlayer.setPlayerName(pParam[0])
        NPlayer.moveTo( int(pParam[2]), int(pParam[3]) )


    def updatePos(self, pID, pParam):

        p = self.playerList.getPlayer(pID)
        if p:
            p.moveTo( int(pParam[0]), int(pParam[1]) )


    def updateCatchStatus(self, pID, pParam):
        """
        Cette fonction met à jour les Statuts des joueur
        attrapeur (pID) et attrapé (pParam[1])
        """

        p = self.playerList.getPlayer(pID)
        p.setPlayerAttrape(int(pParam[0]))
        p.isDirty = False
        p.isGfxDirty = True

        p = self.playerList.getPlayer(int(pParam[0]))
        p.setPlayerStatus('A')
        p.isGfxDirty = True





    def receptionMessage(self):

        ret = LVGNetLib.DecodeMessage()

        if type(ret) == list:

            # Message a traiter
            if len(ret) > 0:
                for m in ret:
                    print("Msg de [%6d] : [%10s] : %s"%(m['id'],m['inst'],m['params']))

                    if m['inst'] == 'M':
                        print("[i] Joueur Local inscrit avec l'ID %d"%(m['id'],))
                        self.playerList.LocalPlayerID = m['id']
                        # Envoie de la commande du Type choisi
                        LVGNetLib.Send('T:'+self.LPType)

                    elif m['inst'] == 'ND':
                        # Mise à jour de la liste des joueurs
                        self.checkPlayerList(m['id'],m['params'] )

                    elif m['inst'] == 'N':
                        # Récupère le pédigré du joueur
                        LVGNetLib.Send('L:'+str(m['id']))

                    elif m['inst'] == 'C':
                        self.updateCatchStatus(m['id'], m['params'])

                    elif m['inst'] == 'POS':
                        self.updatePos(m['id'], m['params'])


            return True

        # Affichage des messages
        if type(ret) == str:
            print("MSG> ", ret)
            return True

        elif ret == -1:
            return False

    # ========================[ Déplacement Joueur]==================================
    def playerMoveX(self,dx):

        p = self.playerList.getLocalPlayer()
        if p and self._Map._Map.checkMoveTo(p, p.x +dx, p.y):  # MAJ
            LVGNetLib.Send('X:'+str(dx))


    def playerMoveY(self,dy):

        p = self.playerList.getLocalPlayer()
        if p  and self._Map._Map.checkMoveTo(p, p.x, p.y + dy): # MAJ
            LVGNetLib.Send('Y:'+str(dy))


    # ======================[ Action du joueur local ]===============================
    def playerCatch(self):

        print("playerCatch")

        p = self.playerList.getLocalPlayer()

         # MAJ ======================================================

        pList = None

        if (p.dir == 'N') and (p.y > 0):
            pList = self.playerList.findPlayerHorizontal(p.x, p.y-1)
        elif (p.dir == 'S') and (p.y < self._Map._Map.LY-1):
            pList = self.playerList.findPlayerHorizontal(p.x, p.y+1)
        elif (p.dir == 'E') and (p.x < self._Map._Map.LX-1):
            pList = self.playerList.findPlayerVertical(p.x+1, p.y)
        elif (p.dir == 'O') and (p.x > 0):
            pList = self.playerList.findPlayerVertical(p.x-1, p.y)

        # Determination de qui attrappe qui
        if p.typePlayer == 'P':
            fType = 'V'
        elif p.typePlayer == 'R':
            fType = 'P'
        elif p.typePlayer == 'V':
            fType = 'R'

        thePlayer = None

        if pList:
            # Recherche du premier player valable
            for ap in pList:
                if ap._isLocal:
                    continue
                if ap.typePlayer == fType:
                    thePlayer = ap
                    break

        if thePlayer:
            print("Joueur %s attrappé"%(thePlayer.playerName))

            # Met à jour le joueur attrappé
            if thePlayer.testPlayerStatus('A'):
                LVGNetLib.Send('C:'+str(thePlayer.ID))
                #p.setPlayerAttrape(thePlayer.ID)

        else:
            print("aucun joueur attrappé")





    # ==================================[ Gfx Fonction ]=============================

    def renderPlayer(self):
        """
        Dessine les joueur sur le plateau
        """

        for p in self.playerList.PlayerList:
            p.Draw(self._Screen, self._Map)


    def render(self):

        pygame.time.delay(20)

        # Vérifie si il faut redessiner le fond
        if self.bgHasChanged:
            self._Screen.drawBackground(self._Map._Map.Theme)
            self.bgHasChanged = False

        # Récupère le jeur local
        lPlayer = self.playerList.getLocalPlayer()

        if lPlayer:
            (x,y) = lPlayer.getPos()
        else:
            x = -1
            y = -1

        # Redessine la Map de Base => retourne l'offset x,y (ox,oy)
        self._Map.DessineTout(x,y)

        # Dessine les joueurs
        self.renderPlayer()

        # Captures des évènements
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return(False)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    self.playerMoveX(-1)
                    continue
                elif event.key == pygame.K_RIGHT:
                    self.playerMoveX(1)
                    continue
                elif event.key == pygame.K_UP:
                    self.playerMoveY(-1)
                    continue
                elif event.key == pygame.K_DOWN:
                    self.playerMoveY(1)
                    continue
                elif event.key == pygame.K_LCTRL:
                    self.playerCatch()
                    continue

        # Mise à jour de l'écran
        pygame.display.update()
        return(True)
