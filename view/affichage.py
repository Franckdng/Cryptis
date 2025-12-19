import pygame
import configuration as config


class Affichage:
    """Gère tout l'affichage du jeu.
    Methods:
        __init__: Initialise l'affichage avec l'écran donné.
        dessiner: Dessine l'affichage en fonction de l'état du jeu.
        dessiner_page_garde: Affiche le grand titre au début.
        dessiner_menu: Affiche le menu de sélection de la difficulté.
        dessiner_tutoriel: Affiche les instructions du tutoriel.
        dessiner_duel: Affiche le duel entre le joueur et le bot.
        dessiner_fin: Affiche l'écran de fin avec le résultat.
        dessiner_commandes_jeu: Affiche les commandes en bas de l'écran.
        dessiner_zone: Dessine une zone (joueur ou bot) avec son polynôme et outil.
        dessiner_polynome: Dessine un polynôme à une position donnée.
        dessiner_texte: Dessine un texte à une position donnée.


    """

    def __init__(self, ecran):
        """
        Initialise l'affichage avec l'écran donné.
        Args:
           ecran (pygame.Surface): L'écran où dessiner.
        """
        self.ecran = ecran
        self.police = pygame.font.SysFont("Consolas", 20)
        self.police_titre = pygame.font.SysFont("Impact", 80)
        self.police_sous_titre = pygame.font.SysFont("Impact", 40)
        self.police_menu = pygame.font.SysFont("Consolas", 25, bold=True)

    def dessiner(self, moteur):
        """
        Dessine l'affichage en fonction de l'état du jeu.
        Args:
            moteur (MoteurJeu): Le moteur de jeu contenant l'état actuel.

        """
        # Fond d'écran
        self.ecran.fill(config.COLOR_BG)
        # Dessin selon l'état
        if moteur.etat == config.STATE_SPLASH:
            self.dessiner_page_garde()

        elif moteur.etat == config.STATE_MENU:
            self.dessiner_menu()
        elif moteur.etat == config.STATE_TUTORIAL:
            self.dessiner_tutoriel()
        elif moteur.etat == config.STATE_GAME:
            self.dessiner_duel(moteur)
        elif moteur.etat == config.STATE_END:
            self.dessiner_fin(moteur)

        pygame.display.flip()

    def dessiner_page_garde(self):
        """Affiche le grand titre au début

        Args:
          self: Description

        """
        # Affichage du titre
        titre_shadow = self.police_titre.render("CRYPTRIS", True, (0, 50, 100))
        titre = self.police_titre.render("CRYPTRIS", True, config.COLOR_POS)

        center_x = config.SCREEN_WIDTH // 2
        center_y = config.SCREEN_HEIGHT // 2
        # Affichage avec ombre
        self.ecran.blit(
            titre_shadow, (center_x - titre.get_width() // 2 + 5, center_y - 100 + 5)
        )
        self.ecran.blit(titre, (center_x - titre.get_width() // 2, center_y - 100))
        # Affichage du sous-titre
        sous_titre = self.police_sous_titre.render(
            "- TP de Cryptographie appliquée -", True, config.COLOR_ACCENT
        )
        self.ecran.blit(sous_titre, (center_x - sous_titre.get_width() // 2, center_y))

        # Texte clignotant pour commencer
        blink = (pygame.time.get_ticks() // 500) % 2 == 0
        if blink:
            start = self.police.render(
                "[ APPUYEZ POUR COMMENCER ]", True, config.COLOR_TEXT
            )
            self.ecran.blit(start, (center_x - start.get_width() // 2, center_y + 150))

    def dessiner_menu(self):
        """Affiche le menu de sélection de la difficulté
        Args: self: Description

        """
        # Titre
        titre = self.police_sous_titre.render(
            "SÉLECTION DU NIVEAU", True, config.COLOR_POS
        )
        self.ecran.blit(titre, (config.SCREEN_WIDTH // 2 - titre.get_width() // 2, 150))

        y = 300
        mouse_pos = pygame.mouse.get_pos()
        for nom, taille in config.DIFFICULTES.items():
            rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 150, y, 300, 50)

            survol = rect.collidepoint(mouse_pos)
            color_bg = config.COLOR_ACCENT if survol else (20, 30, 40)
            color_border = config.COLOR_POS if survol else (50, 50, 50)

            pygame.draw.rect(self.ecran, color_bg, rect)
            pygame.draw.rect(self.ecran, color_border, rect, 2)

            txt = self.police_menu.render(nom, True, config.COLOR_TEXT)
            self.ecran.blit(
                txt,
                (
                    rect.centerx - txt.get_width() // 2,
                    rect.centery - txt.get_height() // 2,
                ),
            )
            y += 70

    def dessiner_tutoriel(self):
        """Affiche les instructions basées sur l'article Cryptris
        Args: self: Description

        """
        rect = pygame.Rect(
            100, 80, config.SCREEN_WIDTH - 200, config.SCREEN_HEIGHT - 160
        )
        pygame.draw.rect(self.ecran, (10, 15, 25), rect)
        pygame.draw.rect(self.ecran, config.COLOR_ACCENT, rect, 2)

        titre = self.police_sous_titre.render("COMMENT JOUER ?", True, config.COLOR_POS)
        self.ecran.blit(titre, (config.SCREEN_WIDTH // 2 - titre.get_width() // 2, 100))

        # Texte du tutoriel
        lignes = [
            "OBJECTIF :",
            "Le mur représente du BRUIT (+/-) qui cache le message secret.",
            "Vous devez aplatir le mur pour retrouver la ligne unique du message.",
            "",
            "MÉCANIQUE MATHÉMATIQUE :",
            "1. Les briques de couleurs OPPOSÉES s'annulent (-1 + 1 = 0).",
            "2. Les briques de MÊME couleur s'empilent (-1 - 1 = -2).",
            "",
            "VOTRE ARME (LA CLÉ PRIVÉE) :",
            "Votre clé a une forme spéciale : un grand 'Marteau' (Pic) et du petit bruit.",
            "Utilisez ce Marteau pour écraser les grandes colonnes du mur.",
            "",
            "COMMANDES :",
            "[ <- / -> ] ROTATION : Déplacez la clé sur la colonne à viser.",
            "[ HAUT ]    INVERSION : Changez la polarité (+/-) de votre clé.",
            "            (Si le mur est BLEU, utilisez une clé ROUGE).",
            "[ ESPACE ]  ADDITION : Faites tomber la clé pour réduire le mur.",
            "",
            "ASTUCE GLOUTONNE :",
            "Attaquez toujours la colonne la plus haute avec votre Marteau !",
        ]

        y = 170
        for l in lignes:
            # Couleur différente pour les titres
            if (
                "OBJECTIF" in l
                or "MÉCANIQUE" in l
                or "ARME" in l
                or "COMMANDES" in l
                or "ASTUCE" in l
            ):
                c = config.COLOR_ACCENT
                font = self.police_menu  # Gras
            else:
                c = config.COLOR_TEXT
                font = self.police  # Normal

            txt = font.render(l, True, c)
            self.ecran.blit(txt, (rect.x + 40, y))
            y += 30

        # Pied de page
        start = self.police.render(
            "[ CLIQUEZ POUR CRÉER VOTRE CLÉ ]", True, config.COLOR_POS
        )
        self.ecran.blit(
            start, (config.SCREEN_WIDTH // 2 - start.get_width() // 2, rect.bottom - 40)
        )

    def dessiner_duel(self, moteur):
        """Affiche le duel entre le joueur et le bot
        Args:
            self: Description
            moteur: Description

        """

        pygame.draw.line(
            self.ecran,
            (50, 50, 50),
            (config.SCREEN_WIDTH // 2, 0),
            (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 60),
            2,
        )

        # Coté Joueur (Gauche)
        self.dessiner_zone(
            moteur.vecteur_joueur,
            moteur.outil_joueur,
            config.X_PLAYER,
            "JOUEUR",
            config.COLOR_POS,
            config.COLOR_NEG,
            moteur.taille_n,
        )

        # Coté Bot (Droite)
        self.dessiner_zone(
            moteur.vecteur_bot,
            moteur.outil_bot,
            config.X_BOT,
            "BOT (IA)",
            config.COLOR_BOT_POS,
            config.COLOR_BOT_NEG,
            moteur.taille_n,
        )

        # VS au milieu
        vs = self.police_sous_titre.render("VS", True, (100, 100, 100))
        self.ecran.blit(vs, (config.SCREEN_WIDTH // 2 - vs.get_width() // 2, 50))

        # Affiche les coefficients du vecteur joueur en haut à gauche
        coeffs_str = str(moteur.vecteur_joueur.coeffs)
        lbl = self.police.render(
            "DONNÉES CHIFFRÉES (BRUIT):", True, config.COLOR_ACCENT
        )
        self.ecran.blit(lbl, (20, 10))

        police_valeurs = pygame.font.SysFont("Consolas", 14)
        vals = police_valeurs.render(coeffs_str, True, (200, 200, 200))
        self.ecran.blit(vals, (20, 35))

        # Bas de l'écran : commandes
        self.dessiner_commandes_jeu()

        score_txt = self.police.render(
            f"SCORE: {moteur.score}", True, config.COLOR_TEXT
        )
        coups_txt = self.police.render(
            f"COUPS: {moteur.coups_joues}", True, config.COLOR_TEXT
        )
        self.ecran.blit(score_txt, (config.SCREEN_WIDTH - 200, 20))
        self.ecran.blit(coups_txt, (config.SCREEN_WIDTH - 200, 50))

    def dessiner_fin(self, moteur):
        """Affiche l'écran de fin avec le résultat.
        Args: self: Description

        """

        s = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        s.set_alpha(220)
        s.fill((0, 0, 0))
        self.ecran.blit(s, (0, 0))

        # Titre (Victoire ou Défaite)
        if moteur.vainqueur == "JOUEUR":
            txt = "VICTOIRE !"
            col = config.COLOR_POS
            msg_intro = "MESSAGE DÉCHIFFRÉ AVEC SUCCÈS :"
        else:
            txt = "ÉCHEC DE LA MISSION..."
            col = config.COLOR_NEG
            msg_intro = "L'ENNEMI A DÉCHIFFRÉ LE MESSAGE :"

        titre = self.police_titre.render(txt, True, col)
        rect = titre.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 80)
        )
        self.ecran.blit(titre, rect)

        #
        lbl = self.police.render(msg_intro, True, (200, 200, 200))
        rect_lbl = lbl.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)
        )
        self.ecran.blit(lbl, rect_lbl)

        # Message secret
        mot_a_afficher = getattr(moteur, "message_cible", "INCONNU")

        mot_secret = self.police_titre.render(mot_a_afficher, True, config.COLOR_ACCENT)
        rect_mot = mot_secret.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 60)
        )

        pygame.draw.rect(self.ecran, config.COLOR_ACCENT, rect_mot.inflate(40, 20), 2)
        self.ecran.blit(mot_secret, rect_mot)

        # Texte pour rejouer
        info = self.police.render("[ CLIQUEZ POUR REJOUER ]", True, (150, 150, 150))
        self.ecran.blit(
            info, (config.SCREEN_WIDTH // 2 - 120, config.SCREEN_HEIGHT - 100)
        )
        score_final = self.police_sous_titre.render(
            f"SCORE FINAL : {moteur.score}", True, config.COLOR_POS
        )
        rect_score = score_final.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 150)
        )
        self.ecran.blit(score_final, rect_score)

    def dessiner_commandes_jeu(self):
        """Affiche les commandes en bas de l'écran.
        Args: self: Description

        """

        rect_cmd = pygame.Rect(0, config.SCREEN_HEIGHT - 50, config.SCREEN_WIDTH, 50)
        pygame.draw.rect(self.ecran, (0, 0, 0), rect_cmd)
        pygame.draw.line(
            self.ecran,
            config.COLOR_ACCENT,
            (0, config.SCREEN_HEIGHT - 50),
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT - 50),
            1,
        )

        txt = (
            "COMMANDES : [<-/->] BOUGER  |  [HAUT] INVERSER (+/-)  |  [ESPACE] FRAPPER"
        )
        rendu = self.police.render(txt, True, config.COLOR_POS)
        self.ecran.blit(
            rendu,
            (
                config.SCREEN_WIDTH // 2 - rendu.get_width() // 2,
                config.SCREEN_HEIGHT - 35,
            ),
        )

    def dessiner_zone(self, vecteur, outil, center_x, nom, col_pos, col_neg, taille_n):
        """Dessine une zone (joueur ou bot) avec son polynôme et outil.
        Args:
        self: Description
        vecteur: Description
        outil: Description
        center_x: Description
        nom: Description
        col_pos: Description
        col_neg: Description
        taille_n: Description

        """
        # Titre de la zone
        txt_nom = self.police_sous_titre.render(nom, True, col_pos)
        self.ecran.blit(txt_nom, (center_x - txt_nom.get_width() // 2, 50))

        bloc_size = config.BLOCK_SIZE
        margin = config.MARGIN
        start_x = center_x - (taille_n * (bloc_size + margin)) // 2

        # Affiche les valeurs des coefficients sous chaque bloc
        for i in range(taille_n):
            x = start_x + i * (bloc_size + margin)
            rect_fond = pygame.Rect(x, 150, bloc_size, config.BASE_LINE_Y - 150)
            pygame.draw.rect(self.ecran, (20, 30, 40), rect_fond)
            pygame.draw.rect(self.ecran, (40, 50, 60), rect_fond, 1)

            val = vecteur.coeffs[i]
            if val != 0:
                police_val = pygame.font.SysFont("Arial", 12, bold=True)
                txt = police_val.render(str(val), True, (150, 150, 150))
                self.ecran.blit(
                    txt,
                    (x + bloc_size // 2 - txt.get_width() // 2, config.BASE_LINE_Y + 5),
                )

        self.dessiner_polynome(
            vecteur, config.BASE_LINE_Y, False, bloc_size, start_x, col_pos, col_neg
        )
        self.dessiner_polynome(outil, 180, True, bloc_size, start_x, col_pos, col_neg)

    def dessiner_polynome(
        self, poly, y_base, est_joueur, bloc_size, start_x, col_pos, col_neg
    ):
        """Dessine un polynôme à une position donnée.
        Args:
            self: Description
            poly: Description
            y_base: Description
            est_joueur: Description
            bloc_size: Description
            start_x: Description
            col_pos: Description
            col_neg: Description

        """
        if poly is None or not hasattr(poly, "coeffs"):
            return

        coeffs = poly.coeffs
        for i, val in enumerate(coeffs):
            if val == 0:
                continue

            x = start_x + i * (bloc_size + 4)
            hauteur = min(abs(val), 14)
            c = col_pos if val > 0 else col_neg
            direction = 1 if est_joueur else -1
            y_start = y_base if est_joueur else y_base - bloc_size

            for k in range(hauteur):
                y = y_start + (k * direction * bloc_size)
                r = pygame.Rect(x, y, bloc_size, bloc_size)
                pygame.draw.rect(self.ecran, c, r)
                pygame.draw.rect(self.ecran, (0, 0, 0), r, 1)
