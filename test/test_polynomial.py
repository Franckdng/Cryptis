import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.polynomial import Polynome


def test_tout():
    """
    Lance tous les tests unitaires pour la classe Polynome.
    Returns:
        None
    """
    print("--- Démarrage des tests ---")

    # 1. Test Initialisation (Correction : taille au lieu de size)
    p1 = Polynome([1, 2, 3], taille=4)
    assert p1.coeffs == [1, 2, 3, 0], "Erreur init padding"
    print("✅ Init OK")

    # 2. Test Addition
    p2 = Polynome([1, 1, 1, 1], taille=4)
    somme = p1.addition(p2)
    assert somme.coeffs == [2, 3, 4, 1], f"Erreur addition: {somme}"
    print("✅ Addition OK")

    # 3. Test Rotation
    rot = p1.rotation(1)
    assert rot.coeffs == [0, 1, 2, 3], f"Erreur rotation droite: {rot}"

    rot_g = p1.rotation(-1)
    assert rot_g.coeffs == [2, 3, 0, 1], f"Erreur rotation gauche: {rot_g}"
    print("✅ Rotation OK")

    # 4. Test Inversion
    inv = p1.inversion()
    assert inv.coeffs == [-1, -2, -3, 0], "Erreur inversion"
    assert p1.coeffs == [1, 2, 3, 0], "Erreur: L'inversion a modifié l'original !"
    print("✅ Inversion OK")

    # 5. Test Multiplication
    pa = Polynome([1, 1, 0, 0], taille=4)
    pb = Polynome([1, -1, 0, 0], taille=4)
    pmult = pa.multiplication(pb)
    assert pmult.coeffs == [1, 0, -1, 0], f"Erreur Multiplication: {pmult}"
    print("✅ Multiplication (Convolution) OK")

    # 6. Test is_clean
    dirty = Polynome([5, 0, 1, 0], taille=4)
    clean = Polynome([1, -1, 0, 0], taille=4)
    assert dirty.is_clean == False, "Le polynôme bruité devrait être False"
    assert clean.is_clean == True, "Le polynôme propre devrait être True"
    print("✅ is_clean OK")

    print("\n🎉 TOUS LES TESTS SONT PASSÉS ! 🎉")


if __name__ == "__main__":
    test_tout()
