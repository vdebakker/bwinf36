class Punkt:
    """
    Stellt einen Punkt dar, der eine x- und y-Koordinate hat.
    Zwei Punkte werden als gleich angesehen,
    wenn beide Koordinaten gleich sind.
    """
    def __init__(self, x, y):
        self.x = x  # x-Koordinate
        self.y = y  # y-Koordinate
        self.pos = (x, y)

    def __hash__(self):
        return hash(self.pos)  # Hash-Wert um in Set speichern zu können

    def __eq__(self, other):
        # Zwei Punkte sind gleich, falls beie Koordinaten gleich sind
        return self.pos == other.pos

    def __repr__(self):
        # Ausgabe erfolgt in der Form: (x, y)
        return "(%.2f, %.2f)" % (self.x, self.y)
