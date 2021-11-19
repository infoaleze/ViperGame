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
    pass



# ==================================================================
# ==                INITIALISATION Du RESEAU                      ==
# ==================================================================


VGLib.Connect('localhost')




def CheckPalyerList(pID, pParam):

    global playerGroupe

    # pParam = <Name>:<Type>:<X>:<Y>:<Score>





# ==================================================================
# ==        G E S T I O N   D E S    M E S S A G E S              ==
# ==================================================================
def ReceptionMessage():

    global run


    ret = VGLib.DecodeMessage()

    if type(ret) == list:

        # Message a traiter
        if len(ret) > 0:
            for m in ret:
                print("Msg de [%6d] : [%10s] : %s"%(m['id'],m['inst'],m['params']))


        return

    # Affichage des messages
    if type(ret) == str:
        print("MSG> ", ret)

    elif ret == -1:
        run = False


    pass





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
    


# ==========================================================================
# ==               B O U C L E   P R I N C I P A L E
# ==========================================================================

run = True

while run:
    pygame.time.delay(100)


    ReceptionMessage()

    Redessine()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False




pygame.quit()

