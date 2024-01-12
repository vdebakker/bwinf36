from Strecke import *
from Dreieck import *
from Punkt import *

from time import clock
from matplotlib import pyplot as plt


def teilstrecken(punkte: iter):
    """
    Erstellt alle Strecken zwischen allen übergebenen Punkten.
    Dabei werden stets zwei unterschiedliche Punkte genommen
    und eine Streck zwischen ihnen erstellt.
    Am Ende werden alle Strecken zurückgegeben.

    :param punkte 'iter': Eckpunkte der Strecken
    :return: 'set' : alle Teilstrecken
    """
    # Set wird erstellt, in dem alle Strecken gespeichert werden
    # Ein Set wird genommen, da die Reihenfolge keine Rolle spielt
    # und doppelte Strecken so leicht vermieden werden
    strecken = set()
    for erster_punkt in punkte:  # Erster Eckpunkt einer Strecke
        for zweiter_punkt in punkte:  # Zweiter Eckpunkt einer Strecke
            # Bei gleichen Punkten wird keine Strecke erstellt
            if erster_punkt != zweiter_punkt:
                # Neue Strecke wird erstellt und hinzugefügt
                strecken.add(Strecke(erster_punkt, zweiter_punkt))
    return strecken


def dreieckKombinationen(startpunkt: Punkt, verbindungen: list,
                         teilstrecken: set):
    """
    Findet alle Dreiecke die vom übergebenen Startpunkt ausgehen.
    Dabei werden stets zwei Verbindungspunkte von diesem Startpunkt genommen.
    Falls es eine Strecke zwischen diesen Punkten gibt,
    ist ein Dreieck gefunden. Wenn alle Kombinationen von
    Verbindungspunkten überprüft wurden,
    sind alle Dreiecke mit dem übergebenen Startpunkt gefunden.
    :param startpunkt 'class': Startpunkt für das Dreieck
    :param verbindungen 'list': Liste mit Punkten,
    die mit den Starpunkt verbunden sind
    :param teilstrecken 'list': Alle Teilstrecken der Anfangsstrecken
    :return:
    """
    dreiecke = []  # Liste, in der die Dreiecke gespeichert werden
    # Alle Punkte werden aufgerufen
    for i, punkt1 in enumerate(verbindungen[:-1]):
        # Erste Strecke des potenziellen Dreiecks wird berechnet
        strecke1 = Strecke(startpunkt, punkt1)
        # Alle Punkte nach punkt1 werden aufgerufen,
        # damit jede Kombination von zwei Punkten nur einmal aufgerufen wird
        for punkt2 in verbindungen[i + 1:]:
            # Strecke, die nötig wäre um das Dreieck komplett zu machen,
            # wird berechnet
            noetige_strecke = Strecke(punkt1, punkt2)

            # Falls die nötige Strecke existiert,
            # wird ein neues Dreieck hinzugefügt
            # Strecke existirt, wenn sie in allen Teilstrecken enthalten ist
            if noetige_strecke in teilstrecken:
                # Erste Strecke des potenziellen Dreiecks wird berechnet
                strecke2 = Strecke(startpunkt, punkt2)

                # Set mit Eckpunkten wird erstellt
                eckpunkte = {startpunkt, punkt1, punkt2}

                # Liste mit Eckpunkten wird berechnet
                strecken = (strecke1, strecke2, noetige_strecke)

                # Neues Dreieck wird erstellt und
                # zu allen Dreiecken hinzugefügt
                dreiecke.append(Dreieck(strecken, eckpunkte))
    return dreiecke

clock()

""" Eingabe einlesen """

input = open("dreiecke.txt").readlines()  # Inputtext
anzahl_strecken = int(input[0])  # Anzahl der Anfangsstrecken

anfangs_strecken = []  # Liste mit Anfangsstrecken
for i in range(anzahl_strecken):
    # X- und Y-Koordinaten der Endpunkte der Strecke
    x1, y1, x2, y2 = input[i + 1].split()
    punkt1 = Punkt(float(x1), float(y1))  # Erster Endpunkt
    punkt2 = Punkt(float(x2), float(y2))  # Zweiter Endpunkt
    # Neue Strecke wird zu allen Strecken hinzugefügt
    anfangs_strecken.append(Strecke(punkt1, punkt2))

""" Schnittpunkte finden """

schnittpunkte = set()  # Set mit allen Schnittpunkten zwischen den Strecken

# Dictionary wird erstellt mit Strecke als Key und Schnittpunkten
# auf dieser Strecke als Value. Mit diesem Dictionary kann später
# die Strecke leicht in Teilstrecken unterteilt werden
strecken_punkte = {strecke: set() for strecke in anfangs_strecken}

# Alle Strecken außer die letzte Strecke werden geladen
for i, strecke1 in enumerate(anfangs_strecken[:-1]):
    # Alle Strecken nach der ersten Strecke werden galaden,
    # damit keine Schnittpünkte doppelt berechnet werden müssen
    for strecke2 in anfangs_strecken[i + 1:]:
        # Potenzieller Schnittpunkt
        # Dieser ist None, falls es keinen Schnittpunkt gibt
        schnittpunkt = strecke1.schnittpunkt(strecke2)
        if schnittpunkt is not None:  # Es gibt einen Schnittpunkt
            # Schnittpunkten werden beiden Strecken im Dictionary zugeordned
            strecken_punkte[strecke1].add(schnittpunkt)
            strecken_punkte[strecke2].add(schnittpunkt)
            # Schnittpunkt wird zu allen Strecken hinzugefügt
            schnittpunkte.add(schnittpunkt)

""" Strecken entlang der Schnittpunkte teilen """

# Set mit allen Strecken, mit denen Dreiecke gebildet werden können
# Das sind alle Teilstrecken der Anfangsstrecken
alle_strecken = set()
# Alle Schnittpunkte auf einer Strecke werden aufgerufen
for punkte in strecken_punkte.values():
    # Alle Strecken werden um Teilstrecken erweitert
    alle_strecken |= teilstrecken(punkte)

""" Verbindungen zu Punkten zuordnen """

# Dictionary mit Punkt als Key und Liste mit Punkten,
# die mit dem Punkt über eine Strecke verbunden sind, als Value
punkt_verbindungen = {punkt: [] for punkt in schnittpunkte}

for strecke in alle_strecken: # Jeder Punkt wird aufgerufen

    # Verbindungspunkte werden zugeordnet
    punkt_verbindungen[strecke.punkte[0]].append(strecke.punkte[1])
    punkt_verbindungen[strecke.punkte[1]].append(strecke.punkte[0])

""" Dreiecke erstellen """

dreiecke = []  # Liste mit Dreiecken

# Es werden alle Startpunkte und die dazu gehörigen Verbindungpunkte aufgerufen
for startpunkt, verbindungen in punkt_verbindungen.items():
    # Liste mit Dreiecken wird um Dreieckskombinationen
    # mit Startpunkt und Verbindungspunkten erweitert
    dreiecke += dreieckKombinationen(startpunkt, verbindungen, alle_strecken)

""" Doppelte Dreiecke löschen """

# Liste mit Eckpunkten der Dreiecken wird erstellt
# Dort wird für jedes Dreieck die Eckpunkten hinzugefügt.
# Mit dieser Liste kann überprüft werden, ob ein Dreieck bereits gefunden wurde
# Die Reihenfolge der Eckpunkte spielt keine Rolle,
# da sie im Set gespeichert werden
dreiecke_eckpunkte = []
for d in dreiecke[:]:
    if d.eckpunkte in dreiecke_eckpunkte:
        # Dreieck wurde bereits gefunden und kann desshalb gelöscht werden
        dreiecke.remove(d)
    else:
        # Eckpunkte werden der Liste hinzugefügt
        dreiecke_eckpunkte.append(d.eckpunkte)

""" Dreiecke löschen, deren Strecken auf einer Linie sind """

for d in dreiecke[:]:
    # Beide Steigungen sind nicht vertikal
    if d.strecken[0].steigung is not None and \
                    d.strecken[1].steigung is not None:
        if round(d.strecken[0].steigung, 6) == round(d.strecken[1].steigung, 6):
            # Strecken haben gleiche Steigung, also sind sie auf einer Linie
            dreiecke.remove(d)
    elif d.strecken[0].steigung == d.strecken[1].steigung:
        # Beide Strecken sind vertikal
        dreiecke.remove(d)

""" Ergebnisse ausgeben """

output_datei = open("loesung.txt", "w")

print(len(dreiecke), file=output_datei)
for d in dreiecke:
    print(*d.eckpunkte, file=output_datei)

print("Zeit: %.4f" % clock())

""" Dreiecke zeichnen """

# Anfangsdreiecke werden gezeichnet
for strecke in anfangs_strecken:
    punkt1, punkt2 = strecke.punkte
    plt.plot([punkt1.x, punkt2.x], [punkt1.y, punkt2.y], color="b")

# Schnittpunkte werden eingezeichnet
for punkt in schnittpunkte:
    plt.plot(punkt.x, punkt.y, 'ro')

# Strecken der Dreiecke werden eingezeichnet
for d in dreiecke:
    for strecke in d.strecken:
        punkt1, punkt2 = strecke.punkte
        plt.plot([punkt1.x, punkt2.x], [punkt1.y, punkt2.y], color="r")

plt.savefig("graphik.tif")  # Speichern der Figur
