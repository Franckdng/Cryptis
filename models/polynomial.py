class Polynome:
    """
    Représente un polynôme avec des coefficients entiers.
    Attributes:
        coeffs (list of int): Les coefficients du polynôme.
        size (int): La taille du polynôme.
    Methods:
        addition: Additionne deux polynômes.
    """

    def __init__(self, coeffs, taille=16):
        """
        Initialise le polynôme avec les coefficients donnés.
        Args:
            coeffs (list of int): Les coefficients du polynôme.
            taille (int): La taille du polynôme.
        returns:
            None
        """
        self.size = taille

        self.coeffs = list(coeffs)

        # Assure que la taille est correcte
        if len(self.coeffs) < self.size:
            self.coeffs += [0] * (self.size - len(self.coeffs))
        else:
            self.coeffs = self.coeffs[: self.size]

    def __str__(self):
        """

        Représentation en chaîne du polynôme.
        Returns:
            str: La représentation en chaîne des coefficients du polynôme.
        """
        return str(self.coeffs)

    def __repr__(self):
        """
        Représentation en chaîne du polynôme pour le débogage.
        Returns:
            str: La représentation en chaîne des coefficients du polynôme.
        """
        return str(self.coeffs)

    def addition(self, other):
        """
        Additionne deux polynômes.
        Args:
            other (Polynome): Le polynôme à additionner.
        Returns:
            Polynome: Le résultat de l'addition.
        """
        # Vérifie que les tailles sont compatibles
        if len(self.coeffs) != len(other.coeffs):
            raise ValueError("Les polynômes doivent avoir la même taille.")
        # Effectue l'addition coefficient par coefficient
        nouveau_coeffs = [self.coeffs[i] + other.coeffs[i] for i in range(self.size)]
        return Polynome(nouveau_coeffs, self.size)

    def multiplication(self, other):
        """
        Multiplie deux polynômes.
        Args:
            other (Polynome): Le polynôme à multiplier.
        Returns:
            Polynome: Le résultat de la multiplication.
        """
        # Vérifie que les tailles sont compatibles
        if len(self.coeffs) != len(other.coeffs):
            raise ValueError("Les polynômes doivent avoir la même taille.")

        resultat = [0] * self.size
        # Multiplication circulaire
        for i in range(self.size):
            for j in range(self.size):
                valeur = self.coeffs[i] * other.coeffs[j]
                # L'index final en mode circulaire
                index_final = (i + j) % self.size
                resultat[index_final] += valeur
        return Polynome(resultat, self.size)

    def rotation(self, positions):
        """
        Effectue une rotation circulaire des coefficients.
        Args:
            positions (int): Le nombre de positions à faire tourner.
        Returns:
            Polynome: Le polynôme résultant de la rotation.


        """

        # Vérifie que la rotation est correcte
        positions = positions % self.size
        nouveaux = self.coeffs[-positions:] + self.coeffs[:-positions]
        return Polynome(nouveaux, self.size)

    def inversion(self):
        """
        Inverse les signes des coefficients du polynôme.
        Args:
            None
        Returns:
            Polynome: Le polynôme avec les signes inversés.
        """
        nouveaux = [-x for x in self.coeffs]
        return Polynome(nouveaux, self.size)

    def multiplication_scalaire(self, n):
        """
        Multiplie chaque coefficient par un scalaire n.
        Args:
            n (int): Le scalaire par lequel multiplier.
        Returns:
            Polynome: Le polynôme résultant de la multiplication scalaire.
        """
        # Vérifie que n est un entier
        if not isinstance(n, int):
            raise ValueError("Le scalaire doit être un entier.")
        # Effectue la multiplication
        nouveaux_coeffs = [c * n for c in self.coeffs]
        return Polynome(nouveaux_coeffs, self.size)

    def appliquer_modulo(self, mod):
        """
        Réduit chaque coefficient modulo 'mod' avec centrage.
        Args:
            mod (int): Le modulo à appliquer.
        Returns:
            None: Modifie le polynôme en place.

        """
        # Applique le modulo avec centrage
        # Vérifie que la taille est correcte
        if len(self.coeffs) < self.size:
            self.coeffs += [0] * (self.size - len(self.coeffs))
        else:
            self.coeffs = self.coeffs[: self.size]

        nouveaux_coeffs = []
        for c in self.coeffs:
            val = c % mod
            if val > mod // 2:
                val -= mod
            nouveaux_coeffs.append(val)
        self.coeffs = nouveaux_coeffs

    @property
    def is_clean(self):
        """
        Vérifie dynamiquement si le polynôme est propre (coeffs entre -1 et 1).
        Returns:
            bool: True si le polynôme est propre, False sinon.

        """
        return all(abs(coef) <= 1 for coef in self.coeffs)
