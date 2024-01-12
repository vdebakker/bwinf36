class Kante:
    """ Stellt eine Kante dar. Es werden Anfang und Ende der Kante
    gespeichert. Die Positionen der anliegenden Felder werden berechnet.
    """


    def __init__(self, kantepos1, kantepos2):
        # Positionen werden nach x bzw. y-Koordinate sortiert abgespeichert
        if kantepos1[0] < kantepos2[0] or kantepos1[1] < kantepos2[1]:
            self.kantepos1 = kantepos1  # Anfang der Kante
            self.kantepos2 = kantepos2  # Ende der Kante
        else:
            self.kantepos1 = kantepos2
            self.kantepos2 = kantepos1

    def horizontal(self):
        return self.kantepos1[1] == self.kantepos2[1]

    def feld1(self):
        # Feld über bzw. links neben der Kante wird berechnet
        if self.horizontal():
            return self.kantepos1[0], self.kantepos1[1] - 1
        else:
            return self.kantepos1[0] - 1, self.kantepos1[1]

    def feld2(self):
        # Feld unter bzw. rechts neben der Kante wird berechnet
        return self.kantepos1

    def punkte(self):
        return self.kantepos1, self.kantepos2

    def __hash__(self):
        return hash(self.punkte())

    def __eq__(self, other):
        return self.punkte() == other.punkte()