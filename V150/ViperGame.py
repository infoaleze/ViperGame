import VGGfx
import VGNetLib
import VGCore
import os

# ==================================================================
#                               Contantes
# ==================================================================
ServeurIP = "localhost"


# ==================================================================
# ==                INITIALISATION DE PYGAME                      ==
# ==================================================================


VGGfx.LVGNetLib = VGNetLib


baseDir = os.path.dirname(os.path.realpath(__file__))

Ecran = VGGfx.GfxScreenFHD('Viper Game', baseDir)

myMap = VGCore.VMap()
myMap.loadJSON(baseDir + '/Maps/default.json')


GfxMap = VGGfx.GfxMap(myMap)

myGfx = VGGfx.GfxEngine(Ecran,GfxMap)

# Initialisation du réseau
VGNetLib.Connect(ServeurIP)


# Initialisation du joueur Local
myGfx.initialise('Toto', 'P')


# ==========================================================================
# ==               B O U C L E   P R I N C I P A L E
# ==========================================================================

run = True

while run:

    # Reception des messages Réseau
    myGfx.receptionMessage()

    # Actualisation de l'affichage
    run = myGfx.render()

