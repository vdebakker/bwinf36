from Punkt import *


class Strecke:
    """
    Repräsentiert eine Strecke. Diese wird durch ihre zwei Endpunkte dargestellt.
    Um Schnittpunkte zu berechnen werden zusätzlich Steigung
    und Y-Achsenabschnitt berechnet und gespeichert.
    Die Methode schnittpunkt liefert den Schnittpunkt
    zwischen dieser Strecke und einer anderen Strecke
    """

    def __init__(self, punkt1, punkt2):
        # Speichern der Eckpunkte in günstiger Reihenfolge
        # Dies wird gemacht um später leicht zu testen,
        # ob ein Punkt innerhalb der Strecke liegen kann
        # Sie werden zuerst nach x sortiert
        # Dert Punkt mit dem kleinerem x wird zuerst abgespoeichert
        if punkt1.x < punkt2.x:
            self.punkte = (punkt1, punkt2)
        elif punkt1.x > punkt2.x:
            self.punkte = (punkt2, punkt1)
        # Bei gleichem x werden die Punkte nach der y Koordinate sortiert
        # Der Punkt mit kleinerer y-Koordinate wird zuerst gespeichert
        elif punkt1.y < punkt2.y:
            self.punkte = (punkt1, punkt2)
        else:
            self.punkte = (punkt2, punkt1)

        # Steigung berechnen
        if punkt1.x != punkt2.x:
            # Formel für Steigung anwenden
            self.steigung = (punkt2.y - punkt1.y) / (punkt2.x - punkt1.x)
        else:  # Strecke ist vertikal
            self.steigung = None

        # Punkt auf der y-Achse berechnen
        if self.steigung is None:  # Vertikale Strecke
            self.y_achse = None
        else:
            x_abstand_yachse = punkt1.x  # Abstand zur y-Achse
            # Berechnung des y-Achsenabscnitts
            self.y_achse = punkt1.y - self.steigung * x_abstand_yachse

    def schnittpunkt(self, andereStrecke):
        """
        Berechnet den Schnittpunkt von dieser Strecke
        und einer anderen Strecke. Wenn es keinen Schnittpunkt gibt,
        wird (-1, -1) zurückgegeben
        :param andereStrecke 'class': Mit dieser Strecke
        und der eigenen Strecke wird der Schnittpunkt berechnet
        :return: 'class': Schnittpunkt der Klasse Punkt
        Falls es keinen Schnittpunkt gibt wird None zurückgegeben
        """
        if andereStrecke.steigung == self.steigung:  # Parallele Strecken
            # Können keinen Schnittpunkt haben, da sie parallel sind
            return None
        elif self.steigung is None:  # Eigene Strecke ist vertikal
            # mögliche x-Koordinate des Schnittpunkts
            # muss eigene x-Koordinate sein
            x_schnittpunkt = self.punkte[0].x
            # mögiche y-Koordinate des Schnittpunkts
            # wird durch einsetzen der x-Koordinate berechnet
            y_schnittpunkt = andereStrecke.steigung * x_schnittpunkt + \
                             andereStrecke.y_achse

            if not (self.punkte[0].y <= y_schnittpunkt <= self.punkte[1].y):
                # y-Koordinate des Schnittpunkts liegt
                # nicht innnerhalb der ersten Strecke
                return None

        elif andereStrecke.steigung is None:  # Andere Strecke ist vertikal
            # mögliche x-Koordinate des Schnittpunkts
            # muss x-Koordinate der anderen Strecke sein
            x_schnittpunkt = andereStrecke.punkte[0].x
            # mögiche y-Koordinate des Schnittpunkts
            # wird durch einsetzen der x-Koordinate berechnet
            y_schnittpunkt = self.steigung * x_schnittpunkt + self.y_achse

            if not (andereStrecke.punkte[0].y <= y_schnittpunkt <=
                        andereStrecke.punkte[1].y):
                # y-Koordinate des Schnittpunkts liegt
                # nicht innnerhalb der zweiten Strecke
                return None

        else:
            # x-Koordinate des Schnittpunkts wird mit Formel berechnet
            x_schnittpunkt = (andereStrecke.y_achse - self.y_achse) \
                             / (self.steigung - andereStrecke.steigung)
            # y-Koordinate wird berechnet durch das Einsetzen
            # in eine beliebige Geradengleichung
            y_schnittpunkt = self.steigung * x_schnittpunkt + self.y_achse

        # Koordinaten werden gerundet
        x_schnittpunkt = round(x_schnittpunkt, 8)
        y_schnittpunkt = round(y_schnittpunkt, 8)

        # Es wird überprüft, ob die x-Koordinate des Schnittpunkts
        # innerhalb der Strecken liegt
        liegetInStrecke1X = self.punkte[0].x <= x_schnittpunkt \
                            <= self.punkte[1].x
        liegetInStrecke2X = andereStrecke.punkte[0].x <= x_schnittpunkt \
                            <= andereStrecke.punkte[1].x

        if not liegetInStrecke1X or not liegetInStrecke2X:
            # Der Schnittpunkt liegt nicht innerhalb einer Strecke.
            # Dadurch gibt es keinen Schnittpunkt
            return None

        return Punkt(x_schnittpunkt, y_schnittpunkt)

    def __hash__(self):
        # Hash-Wert um Strecken in einem Set zu speichern
        return hash(self.punkte)

    def __eq__(self, other):
        # Strecken werden als gleich angesehen,
        # wenn deren Endpunkte gleich sind
        return self.punkte == other.punkte
