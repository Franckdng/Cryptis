import unittest
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


from cryptographie.transcodeur import Transcodeur


class TestTranscodeur(unittest.TestCase):

    def test_mot_ok_authentique(self):
        """
        Vérifie que le transcodeur respecte bien le codage de l'article pour "OK"
        Args:
            self: instance de la classe de test
        Returns:
            None
        """
        print("\n--- Test Transcodeur Authentique ---")

        # Action
        res = Transcodeur.transcoder("OK", size=8)
        attendu = [0, -1, -1, 1, -1, 0, -1, 1]

        print(f"Mot 'OK' attendu : {attendu}")
        print(f"Mot 'OK' reçu    : {res.coeffs}")

        # Vérification
        self.assertEqual(res.coeffs, attendu)

        # Si on arrive ici, c'est que c'est bon !
        print("✅ SUCCÈS : Le transcodage du texte respecte l'article.")

    def test_nettoyage_valeurs(self):
        """Vérifie que le transcodeur nettoie bien les valeurs bruitées
        Args:
            self: instance de la classe de test
            Returns:
                None"""
        print("\n--- Test Nettoyage des Valeurs ---")

        # Entrée : des valeurs "sales" (ex: 10, -5, 0.1)
        valeurs_sales = [10, -5, 0, 1]
        print(f"Entrée bruitée : {valeurs_sales}")

        # On passe une liste (et pas un str), donc le transcodeur doit nettoyer
        res = Transcodeur.transcoder(valeurs_sales, size=4)

        # Attendu : tout ramené à -1, 0, 1
        attendu = [1, -1, 0, 1]
        print(f"Sortie nettoyée : {res.coeffs}")

        # Vérification
        self.assertEqual(res.coeffs, attendu)

        # Validation visuelle
        print("✅ SUCCÈS : Le nettoyage des valeurs fonctionne.")


if __name__ == "__main__":
    unittest.main()
