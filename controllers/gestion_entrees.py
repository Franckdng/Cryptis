import pygame
import configuration as config


class GestionnaireEntrees:
    """Gère les entrées du clavier et de la souris.
    Le jeu interroge cette classe pour savoir ce que l'utilisateur a fait.

    Methods:
        get_command: Retourne la commande actuelle sous forme de dictionnaire.

    """

    def get_command(self):
        """
        Récupère la commande actuelle de l'utilisateur.
        Args :
            self: Description
        Returns :
            None

        """
        for event in pygame.event.get():

            #  Fermeture de la fenêtre
            if event.type == pygame.QUIT:
                return {"type": "QUIT"}

            # Clique avec la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 = Clic gauche
                    return {"type": "CLICK", "pos": event.pos}

            # Touche du clavier
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    return {"type": "MOVE_LEFT"}

                if event.key == pygame.K_RIGHT:
                    return {"type": "MOVE_RIGHT"}

                if event.key == pygame.K_UP:
                    return {"type": "INVERT"}

                # Espace ou Flèche Bas pour faire descendre le bloc
                if event.key == pygame.K_SPACE or event.key == pygame.K_DOWN:
                    return {"type": "APPLY"}

                # Entrée utilisée surtout dans les menus

                if event.key == pygame.K_RETURN:
                    return {"type": "APPLY"}

        return None
