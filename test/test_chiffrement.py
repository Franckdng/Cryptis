import unittest
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from cryptographie.chiffrement import Chiffrement
from models.polynomial import Polynome


class TestChiffrement(unittest.TestCase):
    """ """

    def test_chiffrer_format(self):
        """
        Teste que le chiffrement renvoie un polynôme valide.
        Args:
            self: instance de la classe de test
        Returns:
            None
        """
        print("\n--- Test Chiffrement ---")

        # Simule une clé publique (taille 4)
        cle_pub = Polynome([1, 0, -1, 0], taille=4)

        # Simule un message à chiffrer (taille 4)
        message = Polynome([1, 1, 0, 0], taille=4)

        # Chiffre
        resultat = Chiffrement.chiffrer(message, cle_pub)

        print(f"Message Clair : {message.coeffs}")
        print(f"Clé Publique  : {cle_pub.coeffs}")
        print(f"Chiffré (C)   : {resultat.coeffs}")

        # Vérifie que le résultat est un polynôme de la bonne taille
        self.assertEqual(len(resultat.coeffs), 4)
        self.assertIsInstance(resultat, Polynome)

        print("✅ Le chiffrement renvoie bien un polynôme valide.")


if __name__ == "__main__":
    unittest.main()
