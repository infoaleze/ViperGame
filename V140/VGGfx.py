import pygame

import VGCore

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
        self.setImage()

    def setTypePlayer(self, TPlayer):

        VGCore.VPlayer.setTypePlayer(self, TPlayer)
        self.setImage()


    def setImage(self):
        """
        Fonction assurant le chargement du sprite correspondant
        en fonction du type de joueur, et si il est local ou pas
        """

        if self._isLocal:

            if self.typePlayer == 'P':
                self.image = pygame.image.load("./images/PouleL.png")
            elif self.typePlayer == 'R':
                self.image = pygame.image.load("./images/RenardL.png")
            elif self.typePlayer == 'V':
                self.image = pygame.image.load("./images/ViperL.png")
            else:
                self.image = pygame.Surface([25,25])
                self.image.fill(COUL_GRIS)

        else:

            if self.typePlayer == 'P':
                self.image = pygame.image.load("./images/Poule.png")
            elif self.typePlayer == 'R':
                self.image = pygame.image.load("./images/Renard.png")
            elif self.typePlayer == 'V':
                self.image = pygame.image.load("./images/Viper.png")
            else:
                self.image = pygame.Surface([25,25])
                self.image.fill(COUL_GRIS)

    def Draw(self,myScreen, myMap):
        """
        Fonction qui dessine le joueur à dans le context graphique
        passé en paramètre.
        """

        if myMap.isVisible(self.x, self.y):

            pass
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!  AJOUTER LE CODE POUR DESSINER le JOUEUR    !!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


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
                    pass
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # !! AJOUTER LE CODE .....
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                #Est un camp ?
                elif ((code & 0x03) > 0):
                    # C'est un camp
                    pass
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # !! AJOUTER LE CODE .....
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


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

        pass
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !! AJOUTER LE CODE .....
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



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


    def initialise(self, Pname, Ptype):

        LPlayer = GfxPlayer()
        LPlayer.setTypePlayer(Ptype)
        LPlayer.setIsLocal(True)
        LPlayer.setPlayerName(Pname)
        LPlayer.ID = -1

        LPlayer.x = 5
        LPlayer.y = 5



        self.playerList.addLocalPlayer(LPlayer)



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

            key = pygame.key.get_pressed()

            if key[pygame.K_LEFT]:
                lPlayer.x -= 1
            if key[pygame.K_RIGHT]:
                lPlayer.x += 1
            if key[pygame.K_UP]:
                lPlayer.y -= 1
            if key[pygame.K_DOWN]:
                lPlayer.y += 1

        # Mise à jour de l'écran
        pygame.display.update()
        return(True)
