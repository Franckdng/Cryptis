import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from cryptographie.gestion_cles import GestionnaireCles
from models.polynomial import Polynome


class TestGestionCles(unittest.TestCase):
    """
    Teste la génération des clés privée et publique.
    Args:
        self: instance de la classe de test
    Returns:
        None
    """

    def test_generation_separee(self):
        """Teste la génération séparée des clés privée et publique.
        Args:
            self: instance de la classe de test
            Returns:
                None"""
        print("\n--- Test Génération Séparée des Clés ---")

        # Configuration initiale
        taille_test = 8
        pic_test = 5
        gestionnaire = GestionnaireCles(taille=taille_test, val_pic=pic_test)

        # Teste la génération de la clé privée
        cle_privee = gestionnaire.generer_cle_privee()

        print(f"Clé Privée : {cle_privee.coeffs}")

        # vérifier qu'elle existe
        self.assertIn(
            pic_test,
            cle_privee.coeffs,
            f"Erreur : Le Pic ({pic_test}) est introuvable dans la clé privée !",
        )
        # Vérifier qu'elle a la bonne taille
        self.assertEqual(
            len(cle_privee.coeffs), taille_test, "Erreur taille clé privée"
        )

        print("✅ Clé Privée générée correctement.")

        # Teste la génération de la clé publique
        cle_publique = gestionnaire.generer_cle_publique(cle_privee)

        print(f"Clé Publique : {cle_publique.coeffs}")

        # Vérifie de la clé publique
        self.assertIsInstance(cle_publique, Polynome)
        self.assertEqual(
            len(cle_publique.coeffs), taille_test, "Erreur taille clé publique"
        )

        # Vérifie que la clé publique est différente de la privée
        self.assertNotEqual(
            cle_publique.coeffs,
            cle_privee.coeffs,
            "Erreur : La clé publique n'est pas brouillée !",
        )

        print("✅ Clé Publique générée et dérivée de la privée.")


if __name__ == "__main__":
    unittest.main()
