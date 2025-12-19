from models.polynomial import Polynome


class Transcodeur:
    """
    Gère le transcodage entre texte et polynôme.
    Methods:
        transcoder: Transcode le message entre texte et polynôme.
        decoder: Opération inverse du transcodage, de polynôme à texte.
    Notes:
    Chaque caractère est converti en une suite de 4 trits (-1, 0, 1).
    """

    CHAR_MAP = {
        "A": [1, 0, 0, 0],
        "B": [-1, 1, 0, 0],
        "C": [0, 1, 0, 0],
        "D": [1, 1, 0, 0],
        "E": [-1, -1, 1, 0],
        "F": [0, -1, 1, 0],
        "G": [1, -1, 1, 1],
        "H": [-1, -1, 1, 1],
        "I": [0, 0, -1, 1],
        "J": [1, 0, -1, 1],
        "K": [-1, 0, -1, 1],
        "L": [0, 1, -1, 1],
        "M": [1, 1, -1, 1],
        "N": [-1, -1, -1, 1],
        "O": [0, -1, -1, 1],
        "P": [1, -1, -1, 1],
        "Q": [-1, -1, -1, 1],
        "R": [0, 0, 0, -1],
        "S": [1, 0, 0, -1],
        "T": [-1, 1, 0, -1],
        "U": [0, 1, 0, -1],
        "V": [1, 1, 0, -1],
        "W": [-1, -1, 1, -1],
        "X": [0, -1, 1, -1],
        "Y": [1, -1, 1, -1],
        "Z": [-1, -1, -1, -1],
        " ": [0, 0, 0, 0],
    }

    def __init__(self, message, size=32):
        """
        Initialise le transcodeur avec le message et la taille du polynôme.
        Args:
            message (str or Polynome): Le message à transcoder.
            size (int): La taille du polynôme résultant.
        """
        self.message = message
        self.size = size

    @staticmethod
    def transcoder(message, size=32):
        """
        Transcode le message entre texte et polynôme.
        Args:
            message (str or Polynome): Le message à transcoder.
            size (int): La taille du polynôme résultant.
        Returns:
            Polynome: Le polynôme résultant du transcodage.
        """
        # Traduis le message en polynôme
        if isinstance(message, str):
            coeffs = []
            for char in message.upper():
                trits = Transcodeur.CHAR_MAP.get(char, [0, 0, 0, 0])
                coeffs.extend(trits)
            return Polynome(coeffs, size)

        # Nettoie le polynôme pour qu'il soit "propre"
        else:
            raw_data = message.coeffs if hasattr(message, "coeffs") else message
            poly_brut = Polynome(raw_data, size)
            coeffs_propres = []
            for coef in poly_brut.coeffs:
                if coef >= 1:
                    coeffs_propres.append(1)
                elif coef <= -1:
                    coeffs_propres.append(-1)
                else:
                    coeffs_propres.append(0)
            return Polynome(coeffs_propres, size)

    @staticmethod
    def decoder(polynome):
        """
        C'est l'opération inverse du transcodage, de polynôme à texte.
        Args:
            polynome (Polynome): Le polynôme à transcoder.
        Returns:
            str: Le message resultat du transcodage.
        """
        # Crée la map inverse pour retrouver les caractères
        inverse_map = {tuple(v): k for k, v in Transcodeur.CHAR_MAP.items()}

        coeffs = polynome.coeffs
        message_final = ""

        # Decoupe les coefficients en blocs de 4
        for i in range(0, len(coeffs), 4):
            bloc = tuple(coeffs[i : i + 4])

            # Sécurise : Si le bloc est incomplet, on arrête
            if len(bloc) < 4:
                break

            # Récupère le caractère correspondant
            lettre = inverse_map.get(bloc, "?")
            message_final += lettre

        # Nettoie les espaces en trop
        return message_final.strip()
