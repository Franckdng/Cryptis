import pygame
import random
import configuration as config
from models.polynomial import Polynome
from cryptographie.gestion_cles import GestionnaireCles
from cryptographie.chiffrement import Chiffrement
from cryptographie.transcodeur import Transcodeur


class MoteurJeu:
    """
    Gère la logique principale du jeu.
    Methods:
        __init__: Initialise le moteur de jeu avec les paramètres par défaut.
        demarrer_duel: Lance le duel entre le joueur et le bot.
        bot_ia_jouer: Logique simple pour que le bot joue automatiquement.
        mise_a_jour: Met à jour l'état du jeu en fonction de la commande reçue.
    """

    def __init__(self):
        """Initialise le moteur de jeu avec les paramètres par défaut.
        Args: self: Description
        Returns: Description

        """

        # initialisation des variables du jeu
        self.etat = config.STATE_SPLASH
        self.taille_n = 32
        self.vainqueur = None
        self.bot_timer = 0
        self.taille_temp = 32
        self.score = 0
        self.coups_joues = 0

        self.outil_joueur = None
        self.vecteur_joueur = None
        self.outil_bot = None
        self.vecteur_bot = None
        self.cle_privee = None
        self.cle_publique = None
        self.message_cible = ""

    def demarrer_duel(self):
        """Lance réellement le jeu après le tutoriel.
        Args: self: Description
        Returns: Description

        """

        self.score = 0
        self.coups_joues = 0

        # Taille choisie dans le menu de difficulté
        self.taille_n = self.taille_temp
        self.gestionnaire = GestionnaireCles(self.taille_n, config.KEY_PEAK_VALUE)

        # Génération des clés
        self.cle_privee = self.gestionnaire.generer_cle_privee()
        self.cle_publique = self.gestionnaire.generer_cle_publique(self.cle_privee)

        # Choix d'un mot aléatoire lié à la cryptographie
        self.message_cible = random.choice(
            [
                # --- Concepts de base ---
                "CIPHER",  # Chiffre
                "SECRET",  # Secret
                "ACCESS",  # Accès
                "SECURE",  # Sécurisé
                "KEYGEN",  # Génération de clé
                "ENIGMA",  # La machine célèbre
                # --- Mathématiques (Réseaux Euclidiens) ---
                "VECTOR",  # Vecteur
                "MATRIX",  # Matrice
                "LATTICE",  # Réseau (le cœur de ton projet !)
                "BASIS",  # Base (de vecteur)
                "NOISE",  # Bruit (ce qu'on ajoute pour chiffrer)
                "EUCLID",  # Euclide
                # --- Culture Hacking / Cyberpunk ---
                "HACKER",
                "BREACH",  # Brèche
                "SIGNAL",
                "SYSTEM",
                "BINARY",
                "DECODE",
            ]
        )

        msg_poly = Transcodeur.transcoder(self.message_cible, size=self.taille_n)
        mur_initial = Chiffrement.chiffrer(
            msg_poly, self.cle_publique, self.gestionnaire.q
        )

        # initialisation du joueur
        self.vecteur_joueur = Polynome(list(mur_initial.coeffs), self.taille_n)
        self.outil_joueur = self.cle_privee

        # initialisation du bot
        self.vecteur_bot = Polynome(list(mur_initial.coeffs), self.taille_n)
        self.outil_bot = self.cle_publique

        self.etat = config.STATE_GAME
        self.vainqueur = None

    def bot_ia_jouer(self):
        """Logique simple pour que le bot joue automatiquement.
        Args:
          self: Description
        Returns:
          Description

        """

        mur = self.vecteur_bot.coeffs
        cle = self.outil_bot.coeffs

        # Recherche du coefficient dominant dans la clé et le mur
        index_marteau = 0
        max_cle = 0
        for i, val in enumerate(cle):
            if abs(val) > max_cle:
                max_cle = abs(val)
                index_marteau = i
        index_cible = 0
        max_mur = 0
        for i, val in enumerate(mur):
            if abs(val) > max_mur:
                max_mur = abs(val)
                index_cible = i

        # Mur déjà "propre", rien à faire
        if max_mur == 0:
            return
        # Tant que la clé n'est pas alignée, on la fait tourner
        if index_marteau != index_cible:
            self.outil_bot = self.outil_bot.rotation(1)
        else:
            # Une fois alignée, on choisit l'action la plus efficace
            # (inversion ou addition)
            val_mur = mur[index_cible]
            val_cle = cle[index_marteau]
            # Si les signes sont identiques, inversion plus efficace
            if (val_mur > 0 and val_cle > 0) or (val_mur < 0 and val_cle < 0):
                self.outil_bot = self.outil_bot.inversion()
            else:
                # Sinon on applique directement la clé
                self.vecteur_bot = self.vecteur_bot.addition(self.outil_bot)

    def mise_a_jour(self, commande):
        """
        Met à jour l'état du jeu en fonction de la commande reçue.
        Le jeu est structuré comme une machine à états simples
        (écrans + logique de jeu) pour garder un code lisible.

        Args:
            commande (dict): La commande reçue du gestionnaire d'entrées.
        Returns: None
        """
        if not commande:
            return

        # Sécurité : aucune action possible si la clé joueur n'est pas prête
        if self.etat == config.STATE_GAME and self.outil_joueur is None:
            return

        cmd_type = commande["type"]

        # Ecran de démarrage
        if self.etat == config.STATE_SPLASH:
            if cmd_type == "CLICK" or cmd_type == "APPLY":
                self.etat = config.STATE_MENU

        # Menu de sélection de la difficulté
        elif self.etat == config.STATE_MENU:
            if cmd_type == "CLICK":
                mouse_pos = commande["pos"]
                y = 300
                for nom, taille in config.DIFFICULTES.items():
                    rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 150, y, 300, 50)
                    if rect.collidepoint(mouse_pos):
                        self.taille_temp = taille  # Sauvegarde la taille choisie
                        self.etat = config.STATE_TUTORIAL  # Passe au tuto
                    y += 70

        # Tuto
        elif self.etat == config.STATE_TUTORIAL:
            if cmd_type == "CLICK" or cmd_type == "APPLY":
                self.demarrer_duel()  # Lance le duel

        # Jeu
        elif self.etat == config.STATE_GAME:
            # Commandes de déplacement / modification de l'outil
            if cmd_type == "MOVE_LEFT":
                self.outil_joueur = self.outil_joueur.rotation(-1)
            elif cmd_type == "MOVE_RIGHT":
                self.outil_joueur = self.outil_joueur.rotation(1)
            elif cmd_type == "INVERT":
                self.outil_joueur = self.outil_joueur.inversion()

            # Commande d'action (C'est ici qu'on gère les scores et les coups)
            elif cmd_type == "APPLY":
                # Calcul de la hauteur avant
                hauteur_avant = sum(abs(c) for c in self.vecteur_joueur.coeffs)

                # Application de l'outil
                self.vecteur_joueur = self.vecteur_joueur.addition(self.outil_joueur)
                self.coups_joues += 1

                # Calcul de la hauteur après
                hauteur_apres = sum(abs(c) for c in self.vecteur_joueur.coeffs)

                # Mise à jour du score
                if hauteur_apres < hauteur_avant:
                    # Bonus si on réduit le mur
                    self.score += int((hauteur_avant - hauteur_apres) * 10)
                else:
                    # Malus si on aggrave la situation
                    self.score = max(0, self.score - 5)

            # Tour du bot
            self.bot_timer += 1
            if self.bot_timer >= config.BOT_SPEED:
                self.bot_ia_jouer()
                self.bot_timer = 0

            # Vérification des conditions de victoire
            if self.vecteur_joueur.is_clean:
                self.etat = config.STATE_END
                self.vainqueur = "JOUEUR"
            elif self.vecteur_bot.is_clean:
                self.etat = config.STATE_END
                self.vainqueur = "BOT"

        # Écran de fin
        elif self.etat == config.STATE_END:
            if cmd_type == "CLICK" or cmd_type == "APPLY":
                self.etat = config.STATE_MENU
