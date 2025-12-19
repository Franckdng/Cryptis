from models.polynomial import Polynome


class Dechiffrement:
    """

    Gère le déchiffrement du message.
    Methods:
        dechiffrer: Déchiffre le message chiffré avec la clé privée.
    """

    @staticmethod
    def dechiffrer(message_chiffre, cle_privee):
        """
        Déchiffre le message chiffré avec la clé privée.

        Args:
            message_chiffre (Polynome): Le message chiffré à déchiffrer.
            cle_privee (Polynome): La clé privée utilisée pour le déchiffrement.
        Returns:
            Polynome: Le message déchiffré.
        """
        # Copie de travail pour ne pas modifier le message original
        courant = Polynome(list(message_chiffre.coeffs), message_chiffre.size)

        # Valeur du pic pour les frappes
        force_pic = cle_privee.val_pic

        iteration = 0
        while not courant.is_clean and iteration < 1000:
            # Recherche du coefficient le plus problématique
            pire_val = 0
            pire_idx = 0
            for i, v in enumerate(courant.coeffs):
                if abs(v) > abs(pire_val):
                    pire_val = v
                    pire_idx = i

            # Nombre de frappes nécessaires pour réduire ce pic
            nb_frappes = abs(pire_val) // force_pic
            if nb_frappes == 0:
                nb_frappes = 1

            # Alignement de la clé sur la zone critique
            cle_alignee = cle_privee.rotation(pire_idx)

            # Application des frappes
            if pire_val > 0:
                frappe = cle_alignee.multiplication_scalaire(-nb_frappes)
            else:

                frappe = cle_alignee.multiplication_scalaire(nb_frappes)

            courant = courant.addition(frappe)
            iteration += 1

        return courant
