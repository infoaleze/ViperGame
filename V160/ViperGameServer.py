import VGGfx
import VGServerGfx
import VGServerNetLib
import VGCore
import os


# ==================================================================
# ==                INITIALISATION DE PYGAME                      ==
# ==================================================================

TCP_IP = '0.0.0.0'
TCP_PORT = 2021

baseDir = os.path.dirname(os.path.realpath(__file__))

Ecran = VGGfx.GfxScreenFHD('Viper Game Serveur', baseDir)

myMap = VGCore.VMap()
myMap.loadJSON(baseDir + '/Maps/default.json')


GfxMap = VGGfx.GfxMap(myMap)

myGfx = VGServerGfx.GfxServerEngine(Ecran,GfxMap)


# Initialisation du Serveur
ViperServer = VGServerNetLib.ServeurThread(TCP_IP, TCP_PORT, myGfx)
ViperServer.start()


# ==========================================================================
# ==               B O U C L E   P R I N C I P A L E                      ==
# ==========================================================================

run = True

while run:

    # Reception des messages Réseau
    #VGNetLib.ReceptionMessage()
    VGServerNetLib.SendMessage()

    # Actualisation de l'affichage
    run = myGfx.render()


print("Arrêt des thread réseaux.....")
ViperServer.stop()
print("End")

