class Reihe:
    """ Stellt eine Reihe dar mit
    - ihrer Lage (Höhe) in der Mauer,
    - den bisher für die Reihe verwendeten Blöcke,
    - den noch nicht verwendeten Blöcken,
    - dem Ende der Reihe und
    - der Länge des längsten noch verfügbaren Blocks
    """

    def __init__(self, hoehe, bloecke, verfuegbar):
        self.hoehe = hoehe  # Lage (Höhe) in der Mauer
        self.bloecke = bloecke  # Schon verwendete Blöcke
        self.verfuegbar = verfuegbar  # Noch nicht verwendete Blöcke
        self.ende = 0   # Position des Endes der Reihe

        # Längster Block wird ermittelt
        if len(verfuegbar) != 0:
            self.laengster = max(verfuegbar)
        else:
            self.laengster = 0

    def fuge_pos(self, k):
        # Gibt die Position der k-ten Fuge zurück, d.h. die Summe der Blöcke
        # bis dorthin
        return sum(self.bloecke[:k])