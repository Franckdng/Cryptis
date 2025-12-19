import pygame
import sys
import configuration as config


import configuration as config
from controllers import MoteurJeu, GestionnaireEntrees
from view import Affichage


def main():
    """Point d'entrée principal du jeu.
    Args:
        None
    Returns:
        None

    """
    # Initiealisation de Pygame
    pygame.init()

    # Création de la fenêtre
    ecran = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.TITLE)

    # Horloge pour gérer les FPS (images par seconde)
    horloge = pygame.time.Clock()

    moteur = MoteurJeu()

    vue = Affichage(ecran)

    entrees = GestionnaireEntrees()

    print("--- JEU CRYPTRIS LANCÉ ---")

    running = True
    while running:
        # Gere le cycle principal du jeu
        commande = entrees.get_command()

        # Si on demande à quitter (croix rouge)
        if commande and commande["type"] == "QUIT":
            running = False

        # Met a jour le moteur du jeu avec la commande reçue
        moteur.mise_a_jour(commande)

        # dessine l'état actuel du jeu
        vue.dessiner(moteur)

        # Attend pour maintenir le nombre de FPS
        horloge.tick(config.FPS)

    # Quitte proprement Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
