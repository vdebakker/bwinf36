class Abschnitt:
    """ Stellt einen Wegabschnitt dar mit den benötigten Kosten, um an allen
    Kanten des Abschnitts einen Höhenunterschied von mindestens 1 herzustellen,
    den Feldern entlang des Abschnitts, den Kanten und einer Liste mit
    den Kosten entlang der Kanten
    """
    def __init__(self, kosten, kanten, felder, verschieben):
        self.kosten = kosten  # Kosten für diesen Abschnitt
        self.kanten = kanten  # Liste mit gewählten Kanten
        self.felder = felder  # Felder, die an den Kanten anliegen
        self.verschieben = verschieben  # Liste mit Werten, wieviel Erde
        # entlang der Kanten verschoben wurde (Kosten)

    def copy(self):
        """ Erstellt eine exakte Kopie des Objekts """
        return Abschnitt(self.kosten, self.kanten[:], self.felder.copy(),
                         self.verschieben[:])