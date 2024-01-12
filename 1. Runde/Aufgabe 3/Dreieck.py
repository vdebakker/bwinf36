class Dreieck:
    """
    Stellt ein Dreieck dar. Es besitzt jeweils drei Strecken und Eckpunkte.
    Diese werden beim Erstellen eines Dreiecks gesetzt.
    """
    def __init__(self, strecken, eckpunkte):
        self.strecken = strecken  # Liste mit Strecken des Dreiecks
        self.eckpunkte = eckpunkte  # Liste mit Eckpunkten des Dreiecks
