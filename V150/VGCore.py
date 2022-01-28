
# -*- coding: utf-8 -*-

import json
import random


class VMap:

    def __init__(self) -> None:
        """
        Constructeur de Classe: Cette fonction lance l'initialisation de l'objet.
        """

        self.Nom = ''            # Nom de la Map
        self.FileName = ''       # Nom du fichier
        self.Theme= 'Base'       # Theme des sprites

        self.LX = -1             # Largeur de la Map
        self.LY = -1             # Hauteur de la Map

        self.Carte = None        # byte array de la Map


        # Propriétés d'état de la classe
        self.__isValid = False


    def reInit(self):
        """
        Cette fonction assure la réinitialisation de la Map
        """
        self.Nom = ''            # Nom de la Map
        self.FileName = ''       # Nom du fichier
        self.LX = -1             # Largeur de la Map
        self.LY = -1             # Hauteur de la Map

        self.Carte = None        # byte array de la Map

        # Propriétés d'état de la classe
        self.__isValid = False


    def setLXLY(self,mLX,mLY):
        """
        Cette fonction définit la taille logique de la Map
        et initailise la carte logique
        """
        self.LX = mLX
        self.LY = mLY
        self.Carte = bytearray(self.LX *self.LY)

    def loadJSON(self,fileName):
        """
        Cette fonction assure la lecture d'un fichier au format JSON
        """

        # Réinitialise la Map
        self.reInit()

        f = open(fileName, "r", encoding="utf8")

        data = json.load(f)

        self.Nom              = data['NomCarte']
        self.FileName         = fileName


        # Initialisation des tableaux
        self.setLXLY(len(data['Carte'][0]), len(data['Carte']) )

        # Convertion du labyrinthe Text en format interne
        self._decodeTxtMap(data)


    def _decodeTxtMap(self, data):
        """
        Cette fonction assure le décodage de la map en format texte
        et initialise le format interne

        0x00 : Case vide
        0x01 : Camp Viper
        0x02 : Camp Renard
        0x03 : Camp Poule

        0xFF : Case inaccessible
        """

        CarteTxt = data['Carte']
        VCamp = data['ViperCampCode']
        PCamp = data['PouleCampCode']
        RCamp = data['RenardCampCode']


        # Pour chaque ligne du Labyrinthe
        for ly, ligne in enumerate(CarteTxt):

            # Pour chaque colonne du Labyrinthe
            for lx, car in enumerate(ligne):

                if car == ' ':
                    self.Carte[ly*self.LX + lx] = 0
                elif car == VCamp:
                    self.Carte[ly*self.LX + lx] = 0x01
                elif car == RCamp:
                    self.Carte[ly*self.LX + lx] = 0x02
                elif car == PCamp:
                    self.Carte[ly*self.LX + lx] = 0x03
                elif car not in ('|', '-', '+', 'Z'):
                    self.Carte[ly*self.LX + lx] = 0
                else:
                    # Vérifie les cases à proximité
                    self.Carte[ly * self.LX + lx] = 0xFF

        self.__isValid = True


    def spawnPosFor(self, type):
        """
        Génère des coordonnée d'arrivé dans le jeux en
        fonction du type de joueur
        """

        # Génére la listes des coordonnée en fonction du type

        if type=='V':
            codeType = 0x01
        elif type=='R':
            codeType = 0x02
        elif type=='P':
            codeType = 0x03
        else:
            return(None)

        validePos = []

        for ly in range(self.LY):
            for lx in range(self.LX):

                if self.Carte[ly*self.LX + lx] == codeType:
                    validePos.append( (lx,ly) )

        if len(validePos) > 0:
            return random.choice(validePos)
        else:
            return(None)




class VPlayer:
    """
    Cette classe représente un joueur
    """

    def __init__(self):

        # ID Réseau du joueur, donnée par la serveur
        self.ID = 0
        # Indique si le joueur est un (R)enard, une (P)oule ou une (V)ipère
        self.typePlayer = None

        self.score = 0
        self.playerName = None

        # Indique si le joueur, est le joueur du Client
        # celui qui joue via cette instance de programme
        self._isLocal = False

        # Position du joueur
        self.x = -1
        self.y = -1

    def setTypePlayer(self, TPlayer):
        self.typePlayer = TPlayer

    def setIsLocal(self, isLocal=False):
        self._isLocal = isLocal

    def setPlayerName(self, NomJoeur=None):
        self.playerName = NomJoeur

    def getPos(self):
        return (self.x, self.y)

    def movePos(self, dx=0, dy=0):
        """
        Met à jour les coordonnées de manière diférentielle
        Si pas possible retourne false
        """
        self.x += dx
        self.y += dy
        return True

    def moveTo(self, px, py):
        """
        Met à jour les coordonnées de manière absolue
        Si pas possible retourne false
        """
        self.x = px
        self.y = py
        return True



# ==============================================================================
# == Gestion de la liste des entités                                          ==
# ==============================================================================
class EntityList:

    def __init__(self, Map):

        self._Map = Map
        self.PlayerList = []         # Liste des joueurs
        self.LocalPlayerID = None    # ID Joueur principal
        self._localPlayerIdx = None


    def _FindLocalPlayerIndex(self):
        """
        Cette fonction à pour objectif de rechercher
        le joueur local identifier par l'ID stocké dans
        self.LocalPlayerID
        """

        self._localPlayerIdx = None

        if self.LocalPlayerID is None:
            return(None)

        for i,p in enumerate(self.PlayerList):
            if p.ID == self.LocalPlayerID:
                self._localPlayerIdx = i
                return(i)

        return(None)


    def getLocalPlayer(self):
        """
        Cette fonction à pour objectif de retourner le
        Joueur local
        """

        if self._localPlayerIdx == None:
            return None

        return self.PlayerList[self._localPlayerIdx]


    def addPlayer(self, PlayerObj):

        # Vérification que l'objet est bien un descendant de Player
        if not(isinstance(PlayerObj,VPlayer)):
            return False

        # Vérification que le joueur n'est pas déjà enregistré
        if PlayerObj in self.PlayerList :
            return False

        # Ajout du monstre dans la liste
        self.PlayerList.append(PlayerObj)

        # Mise à jour de l'index du local player
        self._FindLocalPlayerIndex()

        return True

    def addLocalPlayer(self, PlayerObj):
        # Vérification que l'objet est bien un descendant de Player
        if not(isinstance(PlayerObj,VPlayer)):
            return False

        self.LocalPlayerID = PlayerObj.ID

        return self.addPlayer(PlayerObj)


    def deletePlayer(self, PlayerObj):
        """
        Cette fonction supprime un joueur
        :param PlayerObj objet représentant un joueur
        :return True/False
        """

        # Vérification que le joueur n'est pas déjà enregistrer
        if PlayerObj in self.PlayerList:
            # retire de la liste
            self.PlayerList.remove(PlayerObj)
            # Mise à jour de l'index du local player
            self._FindLocalPlayerIndex()
            return True

        return False

    def getPlayer(self, pID):
        """
        Cette fonction retrouve le player par rapport
        à son ID
        """

        for k in self.PlayerList:

            if k.ID==pID:
                return k

        return None

