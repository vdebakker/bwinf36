import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Mauer:
    """ Stellt eine Mauer dar, die aus Reihen mit Blöcken besteht. Dabei
    werden die linke und rechte Hälfte der Mauer getrennt betrachtet.

    Für die Lösung der vorgeschlagenen Erweiterung wird zusätzlich die
    Anzahl an maximalen Lücken gespeichert. Das sind Fugenpositionen, an denen
    keine Fugen vorkommen müssen.
    """

    def __init__(self, max_luecken):
        self.reihen_links = []  # Liste mit Reihen der linken Seite
        self.reihen_rechts = []  # Liste mit Reihen der rechten Seite
        self.max_luecken = max_luecken  # Maximale Anzahl an Lücken

    def letzte_bloecke_hinzufuegen(self, n=0):
        """ Ergänzt in jeder Höhe den jeweils noch fehlenden Block, und zwar
        am Ende der linken Reihe, also in der Mitte der Mauer.
        Bei ungeraden n wird der längste Block an die zweite Stelle
        in die linke Reihe eingefügt.
        """

        # Jede Reihe wird aufgerufen
        for reihe_links in self.reihen_links:
            # Fehlender letzter Block wird hinten an linke Liste angehängt.
            for block in reihe_links.verfuegbar.copy():
                reihe_links.bloecke.append(block)
                reihe_links.verfuegbar.remove(block)

            # Bei ungerader Anzahl an Blöcken wird
            # der längste Block an zweiter Stelle hinzugefügt
            if n % 2 == 1: reihe_links.bloecke.insert(1, n)

    def sortiere(self):
        """ Sortiert die linken und die rechten Reihen jeweils aufsteigend
        nach den Höhen.
        """

        self.reihen_links = sorted(self.reihen_links, key=lambda r: r.hoehe)
        self.reihen_rechts = sorted(self.reihen_rechts, key=lambda r: r.hoehe)

    def zeichne(self, name):
        """ Zeichnet die Mauer und speichert sie unter übergebenen Namen ab

        :param name: Name des entgültigen Bildes
        :return: None
        """
        ax = plt.subplot()

        # Breite der Mauer
        breite = sum(self.reihen_links[0].bloecke) + \
                 sum(self.reihen_rechts[0].bloecke)

        # Momentane Höhe der Mauer
        hoehe = 0

        # Es werden jeweils eine linke Reihe und eine rechte Reihe aufgerufen
        # und gezeichnet
        for reihe_links, reihe_rechts in \
                zip(self.reihen_links, self.reihen_rechts):

            # Alle Blöcke der linken Reihe werden gezeichnet
            for i in range(len(reihe_links.bloecke)):
                # Rechteck wird erstellt
                rect = patches.Rectangle((reihe_links.fuge_pos(i), hoehe),
                                         reihe_links.bloecke[i], 1,
                                         edgecolor='r', facecolor='w')
                ax.add_patch(rect)  # Rechteck wird dem Bild hinzugefügt

                # Länge des Blocks wird ins Feld geschrieben
                plt.text(reihe_links.fuge_pos(i) + reihe_links.bloecke[i] / 2,
                         hoehe + .5, reihe_links.bloecke[i])

            # Alle Blöcke aus rechter Reihe werden gezeichnet
            for i in range(len(reihe_rechts.bloecke)):
                # Rechteck wird erstellt
                rect = patches.Rectangle((breite - reihe_rechts.fuge_pos(i + 1),
                                          hoehe), reihe_rechts.bloecke[i], 1,
                                         edgecolor='r', facecolor='w')
                ax.add_patch(rect)  # Rechteck wird dem Bild hinzugefügt

                # Länge des Blocks wird ins Feld geschrieben
                plt.text(breite - reihe_rechts.fuge_pos(i + 1) +
                         reihe_rechts.bloecke[i] / 2, hoehe + .5,
                         reihe_rechts.bloecke[i])

            hoehe += 1  # Die Höhe wird für die nächste Reihe um 1 erhöht

        # Größe des Koordinatensystems wird gesetzt
        plt.xlim([0, breite])
        plt.ylim([0, hoehe])
        plt.yticks(range(hoehe + 1))
        if breite <= 10: plt.xticks(range(breite + 1))
        elif breite <= 30: plt.xticks(range(0, breite + 1, 5))
        plt.savefig(name)  # Abbildung wird gespeichert
        plt.clf()  # Plot wird geleert für das nächste Bild

    def schreibe(self, name):
        """ Schreibt die Blockbreiten - analog zur graphischen Ausgabe - in
        eine Datei. Jede Zeile steht für eine Reihe in der Mauer.

        :param name: Name, unter dem die Mauer gespeichert werden soll
        :return: None
        """

        datei = open(name, "w")
        for reihe_l, reihe_r in zip(self.reihen_links[::-1],
                                    self.reihen_rechts[::-1]):
            print(*reihe_l.bloecke, *reihe_r.bloecke[::-1], file=datei)
        datei.close()