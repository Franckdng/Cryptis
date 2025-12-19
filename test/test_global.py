import unittest
import sys
import os

# Gestion des chemins pour l'import des modules locaux
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from cryptographie.gestion_cles import GestionnaireCles
from cryptographie.transcodeur import Transcodeur
from cryptographie.chiffrement import Chiffrement
from cryptographie.dechiffrement import Dechiffrement


class TestGlobal(unittest.TestCase):
    """
    Teste l'intégration complète du processus de chiffrement et déchiffrement.
    Args:
        self: instance de la classe de test
    Returns:
        None
    """

    def test_simulation_complete(self):
        print("\n🌐 --- TEST GLOBAL : CHIFFREMENT & DÉCHIFFREMENT --- 🌐")

        # Configuration initiale
        taille_n = 32
        force_pic = 25
        print(f"1️⃣ Génération des clés (N={taille_n})...")

        gestionnaire = GestionnaireCles(taille=taille_n, val_pic=force_pic)
        cle_privee = gestionnaire.generer_cle_privee()
        cle_publique = gestionnaire.generer_cle_publique(cle_privee)

        # Affichage des clés (extraits)
        message_texte = "BRAVO"
        print(f"2️⃣ Message '{message_texte}'...")
        poly_original = Transcodeur.transcoder(message_texte, size=taille_n)
        print(f"   Original (extraits) : {poly_original.coeffs[:8]}...")

        # Chiffre
        print("3️⃣ Chiffrement...")
        # On récupère q depuis le gestionnaire de clés
        q_val = gestionnaire.q

        # passe le polynôme original et la clé publique au chiffrement
        mur_chiffre = Chiffrement.chiffrer(poly_original, cle_publique, q_val)

        self.assertFalse(mur_chiffre.is_clean, "Le mur chiffré devrait être sale !")
        print(f"   Chiffré (mod {q_val}) : {mur_chiffre.coeffs[:8]}...")

        # Déchiffre
        print("4️⃣ Tentative de Déchiffrement...")
        poly_dechiffre = Dechiffrement.dechiffrer(mur_chiffre, cle_privee)
        print(f"   Déchiffré (mod 3) : {poly_dechiffre.coeffs[:8]}...")

        # Vérifications finales

        self.assertTrue(
            poly_dechiffre.is_clean,
            "❌ ECHEC : Le déchiffrement n'a pas nettoyé le message (is_clean est False) !",
        )

        # Compare les coefficients du polynôme original et du polynôme déchiffré
        self.assertEqual(
            poly_dechiffre.coeffs,
            poly_original.coeffs,
            f"❌ ECHEC : Les coefficients ne correspondent pas !\nAttendu : {poly_original.coeffs}\nObtenu   : {poly_dechiffre.coeffs}",
        )

        # C. Retour au texte
        texte_final = Transcodeur.decoder(poly_dechiffre)
        print(f"✅ SUCCÈS : Texte retrouvé -> '{texte_final}'")
        self.assertEqual(message_texte, texte_final)


if __name__ == "__main__":
    unittest.main()
