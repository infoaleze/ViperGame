import VGGfx
import VGCore
import pygame


# ==================================================================
# ==  DEFINTION DE LA CLASSES MOTEUR GRAPHQIUE POUR LE SERVEUR    ==
# ==================================================================
class GfxServerEngine():

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
        self.VGrp = VGCore.EntityList(self._Map)
        self.PGrp = VGCore.EntityList(self._Map)
        self.RGrp = VGCore.EntityList(self._Map)

        self.mapCenterX = 1
        self.mapCenterY = 1



    def initialise(self, Pname, Ptype):

        pass



    def addPlayer(self, pType):
        """
        Ajoute un nouveau joueur
        """

        if pType not in ['V', 'P', 'R']:
            return None

        pTemp =  VGGfx.GfxPlayer()
        pTemp.setTypePlayer(pType)

        res = self._Map._Map.spawnPosFor(pType)
        if res:
            (pTemp.x,pTemp.y) = res

        if pType=='V':
            self.VGrp.addPlayer(pTemp)
        elif pType=='R':
            self.RGrp.addPlayer(pTemp)
        elif pType=='P':
            self.PGrp.addPlayer(pTemp)

        return(pTemp)


    def removePlayer(self, player):

        if player is not None:

            t = player.typePlayer

            if t=='P':
                self.PGrp.deletePlayer(player)
                return(True)
            elif t=='V':
                self.VGrp.deletePlayer(player)
                return(True)
            elif t=='R':
                self.RGrp.deletePlayer(player)
                return(True)

            return(False)

        return(False)

    def renderPlayer(self):
        """
        Dessine les joueur sur le plateau
        """


        for p in self.PGrp.PlayerList:
            p.Draw(self._Screen, self._Map)

        for p in self.VGrp.PlayerList:
            p.Draw(self._Screen, self._Map)

        for p in self.RGrp.PlayerList:
            p.Draw(self._Screen, self._Map)


    def render(self):

        pygame.time.delay(20)

        # Vérifie si il faut redessiner le fond
        if self.bgHasChanged:
            self._Screen.drawBackground(self._Map._Map.Theme)
            self.bgHasChanged = False


        # Redessine la Map de Base => retourne l'offset x,y (ox,oy)
        self._Map.DessineTout(self.mapCenterX,self.mapCenterY)

        # Dessine les joueurs
        self.renderPlayer()

        # Captures des évènements
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return(False)

            key = pygame.key.get_pressed()

            if key[pygame.K_LEFT]:
                self.mapCenterX -= 1
            if key[pygame.K_RIGHT]:
                self.mapCenterX += 1
            if key[pygame.K_UP]:
                self.mapCenterY -= 1
            if key[pygame.K_DOWN]:
                self.mapCenterY += 1

        # Mise à jour de l'écran
        pygame.display.update()
        return(True)