import random
from models.polynomial import Polynome


class Chiffrement:
    """
    Gère le chiffrement du message.
    Methods:
        chiffrer: Chiffre le message avec la clé publique et le modulo q.
    """

    @staticmethod
    def chiffrer(message, poly_publique, q):
        """
        Chiffre le message avec la clé publique et le modulo q.

        Args:
            message (Polynome): Le message à chiffrer sous forme de polyn
            poly_publique (Polynome): La clé publique utilisée pour le chiffrement.
            q (int): Le modulo à appliquer après le chiffrement.

        Returns:
            Polynome: Le message chiffré.
        """

        # Taille du polynome
        taille = poly_publique.size

        # Polynôme aléatoire servant de bruit
        coeffs_a = [random.choice([-1, 0, 1]) for _ in range(taille)]
        a = Polynome(coeffs_a, taille)

        # Création du masque : Masque = a * Publique
        masque = a.multiplication(poly_publique)

        # Le message est caché derrière le masque
        message_chiffre = masque.addition(message)

        # Reduction modulo q
        message_chiffre.appliquer_modulo(q)

        return message_chiffre
