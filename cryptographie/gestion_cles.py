import random
from models.polynomial import Polynome


class GestionnaireCles:
    """
    Gère la génération des clés privées et publiques.
    Methods:
        __init__: Initialise le gestionnaire avec la taille et la valeur du pic.
        generer_cle_privee: Génère une clé privée 'courte' avec un pic central dominant.
        generer_cle_publique: Génère la clé publique à partir de la clé privée.
    """

    def __init__(self, taille=32, val_pic=25):
        """
        Initialise le gestionnaire avec la taille et la valeur du pic.
        Args:
            taille (int): La taille des polynômes (clés).
            val_pic (int): La valeur du pic principal dans la clé privée.
        """

        self.taille = taille
        self.val_pic = val_pic
        # Modulo choisi comme puissance de 2 pour simplifier les calculs
        self.q = 2048

    def generer_cle_privee(self):
        """
        Génère une clé privée 'courte' avec un pic central dominant
        et quelques pics secondaires aléatoires (Style Cryptris).
        Args: self: Description
        Returns:
            Polynome: La clé privée générée.
        """
        # Commence par un polynôme nul
        coeffs_privee = [0] * self.taille

        # Ajoute des pics secondaires aléatoires
        for i in range(self.taille):
            if random.random() < 0.3:
                coeffs_privee[i] = random.choice([-1, 1])

        # Force le pic principal
        coeffs_privee[0] = self.val_pic

        cle_privee = Polynome(coeffs_privee, self.taille)

        # Attache la valeur du pic pour le déchiffrement
        cle_privee.val_pic = self.val_pic

        return cle_privee

    def generer_cle_publique(self, cle_privee):
        """
        Génère la clé publique P = f * g [mod q].
        g est un polynôme aléatoire très bruité.
        Args:
            cle_privee (Polynome): La clé privée utilisée pour générer la clé publique.
        Returns:
            Polynome: La clé publique générée.
        """
        # Polynôme aléatoire très bruité
        coeffs_g = [random.randint(-5, 5) for _ in range(self.taille)]
        g = Polynome(coeffs_g, self.taille)

        # Clé publique : P = f * g mod q
        cle_pub = g.multiplication(cle_privee)

        # Application du modulo q
        cle_pub.appliquer_modulo(self.q)

        return cle_pub
