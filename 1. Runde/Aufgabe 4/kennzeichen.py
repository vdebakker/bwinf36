class Kennzeichen:
    """
    Repräsentiert ein Kennzeichen mit  Stadtkürzel und Buchstaben.
    Die Zahlen werden ignoriert.
    """
    def __init__(self, kuerzel, buchstaben):
        self.kuerzel = kuerzel  # Stadtkürzel aus ein bis drei Buchstaben
        self.buchstaben = buchstaben  # Ein oder zwei frei wählbare Buchstaben

    def __repr__(self):
        # Kennzeichen wird durch Kürzel, Buchstaben und
        # zwei Beispielzahlen repräsentiert
        return str(self.kuerzel) + " " + str(self.buchstaben) + " 00"

    def __len__(self):
        # Länge setzt sich aus Länge des Kürzel und Länge der Buchstaben zusammen
        # Diese Methode wird verwendet um zu überprüfen, ob ein Kennzeichen ein
        # gesamtes Wort darstellt, indem die Längen verglichen werden
        return len(self.kuerzel) + len(self.buchstaben)