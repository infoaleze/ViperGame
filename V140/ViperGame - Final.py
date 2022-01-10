import VGGfx
import VGNetLib
import VGCore
import os

# ==================================================================
# ==                INITIALISATION DE PYGAME                      ==
# ==================================================================


baseDir = os.path.dirname(os.path.realpath(__file__))

Ecran = VGGfx.GfxScreenFHD('Viper Game', baseDir)

myMap = VGCore.VMap()
myMap.loadJSON(baseDir + '/Maps/default.json')


GfxMap = VGGfx.GfxMap(myMap)

myGfx = VGGfx.GfxEngine(Ecran,GfxMap)

myGfx.initialise('Yoann', 'P')

# Initialisation



# ==========================================================================
# ==               B O U C L E   P R I N C I P A L E
# ==========================================================================

run = True

while run:

    # Reception des messages Réseau
    #VGNetLib.ReceptionMessage()

    # Actualisation de l'affichage
    run = myGfx.render()

