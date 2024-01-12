from weg import Weg

from matplotlib import pyplot as plt
from matplotlib import patches as patches





def zeichne(matrix, name, weg=None):
    """ Zeichnet ein Bild von einer übergebenen Matrix.
    Es kann auch ein Weg eingezeichnet werden.
    :param matrix: Matrix mit Höhen der Planquadrate
    :param name: Name der Datei, unter dem das Bild gespeichert werden soll
    :param weg: Weg der eingezeichnet werden soll
    :return: None
    """

    # Liste mit allen Feldhöhen, um minimale und maximale Feldhöhe zu
    # identifizieren
    felder = []
    for reihe in matrix:
        felder.extend(reihe)
    niedrigster = min(felder)  # geringste Höhe
    hoechster = max(felder)  # größte Höhe
    # Differenz der Höhen, um Farbe linear zu skalieren
    diff = hoechster - niedrigster

    ax = plt.subplot()

    # Alle Planquadrate werden aufgerufen
    for x in range(len(matrix)):
        for y in range(len(matrix)):
            hoeher = matrix[y][x] - niedrigster  # Höher als niedrigstes Feld
            if diff != 0:
                hoeher /= diff  # Skalierung zwischen 0 und 1
            # Rechteck wird erstellt
            rect = patches.Rectangle((x, y),
                                     1, 1, facecolor=(hoeher, hoeher, hoeher))
            ax.add_patch(rect)  # Rechteck wird dem Bild hinzugefügt

    if weg:  # Ein Weg wurde angegeben
        # Jeder Abschnitt wird aufgerufen
        for a in weg.abschnitte:
            # Jede Kante wird eingezeichnet
            for k in a.kanten:
                x1, y1 = k.kantepos1
                x2, y2 = k.kantepos2
                # Kante wird als Linie eingezeichnet
                plt.plot([x1, x2], [y1, y2], color="r", linestyle='-',
                         linewidth=3)

        # Gerundete Kosten über das Diagramm schreiben
        plt.title("Kosten: %.4f" % weg.kosten)

    # Größe des Koordinatensystems wird gesetzt
    plt.xlim([0, n])
    plt.ylim([n, 0])
    plt.savefig(name)  # Abbildung wird gespeichert
    plt.clf()  # Plot wird geleert für das nächste Bild


''' Input einlesen '''

datei = "wildschwein5"  # Zu bearbeitende Datei
input = open(datei + ".txt").readlines()  # Inputliste

n = int(input[0])  # Vorgegebenes n
feld = []  # Matrix für die Höhen
for i in range(n):
    reihe = input[i + 1].split(' ')  # Reihe mit Höhen als Strings
    reihe = [float(m) for m in reihe]  # Liste mit Höhen aus Reihe
    feld.append(reihe)

# Ausgangsbild wird gezeichnet
zeichne(feld, datei + ".tif")


''' Minimum berechnen '''

min_benoetigt = []  # Liste mit Minimum aus jeder Spalte
for x in range(n):
    max_diff = 0  # Bisher maximale Differenz
    for y in range(n - 1):
        # Absolute Differenz zweier benachbarter Felder
        diff = abs(feld[y][x] - feld[y + 1][x])
        if diff > max_diff:  # Neue maximale Differenz gefunden
            max_diff = diff

    if max_diff >= 1:
        # Differenz mindestens 1, also muss keine Erde verschoben werden
        min_benoetigt.append(0)
    else:
        # Differenz kleiner 1, also muss Erde verschoben werden
        min_benoetigt.append((1 - max_diff) / 2)

# Liste mit mindestens benötigten Kosten,
# um bei einer bestimmten Position einen Weg bis zum Ende zu erstellen
min_ende = []
for x in range(n + 1):
    # Mindestens benötigte Kosten sind Summe der minimalen Kosten bis zum Ende
    min_ende.append(round(sum(min_benoetigt[x:]), 4))

''' Anfangswege erstellen '''

# Liste mit allen Wegen
wege = []
for i in range(1, n):
    # Neuer Weg, der bei (0, i) startet, wird erstellt und hinzugefügt
    w = Weg([], (0, i), 0, set(), [], min_ende[0])
    wege.append(w)

''' Dictionary, um mehrmals besuchte Stellen zu reduzieren '''

# Dictionary, das sich merken soll, welche Stellen bereits von welchen Wegen
# besucht wurden
# Für jede Stelle wird maximal ein Wege aus einer Richtung gespeichert
besuchte_punkte = {}

# Für jeden Punkt wird ein leeres Dictionary hinzugefügt
for x in range(n + 1):
    for y in range(n + 1):
        besuchte_punkte[(x, y)] = {}

maximum = 0  # Bisher höchste x-Position des Weges (dient zu Testzwecken)

# Lookup Liste, um bestimmte Wegabschnitte nicht doppelt zu berechnen
lookup = []

''' Optimalen Weg finden '''

# Solange der günstigste Weg nicht das Ende erreicht hat, wird weiter gesucht
while wege[-1].ende[0] != n:
    w = wege.pop()  # Der bisher günstigste Weg

    # Alle möglichen nächsten Wege werden aufgerufen
    for w_neu in w.naechste_wege(n, feld, lookup, min_ende):

        if w_neu.ende[0] > maximum:  # Neuer längster Weg gefunden
            print(maximum)
            maximum = w_neu.ende[0]

        # Letzte Kante des neuen Weges
        letzte_kante = w_neu.kanten[-1].punkte()

        # Wenn noch kein Weg zum selben Endpunkt aus der selben Richtung kam
        # oder dieser Weg günstiger als der andere Weg aus der selben
        # Richtung ist, sollte dieser Weg weiter verfolgt werden

        # Wahrheitswert, ob Punkt bereits aus der selben Richtung besucht wurde
        punkt_besucht = letzte_kante in besuchte_punkte[w_neu.ende]
        if punkt_besucht:
            # Wahrheitswert, ob dieser Weg günstiger ist als der andere Weg
            # aus der selben Richtung
            anderer_weg = besuchte_punkte[w_neu.ende][letzte_kante]
            guenstiger = w_neu.kosten_ende < anderer_weg.kosten_ende
        else:
            anderer_weg = None
            guenstiger = None
        if not punkt_besucht or guenstiger:

            ''' Neuer Weg wird hinzugefügt '''

            # Weg wird bei sortierter Liste an richtiger Stelle eingefügt
            i = 0
            while i < len(wege) and wege[i].kosten_ende >= w_neu.kosten_ende:
                i += 1
            wege.insert(i, w_neu)

            if punkt_besucht:
                # Anderer Weg wird aus de Liste entfernt, falls möglich
                try:
                    wege.remove(anderer_weg)
                except ValueError:
                    # Anderer Weg nicht mehr in der Liste vorhanden
                    pass

            besuchte_punkte[w_neu.ende][letzte_kante] = w_neu

bester_weg = wege[-1]  # Günstigster Weg

''' Effizienz des Weges berechnen '''

print(bester_weg.kosten_ende)
diff = 0
for k in bester_weg.kanten:
    x1, y1 = k.feld1()
    x2, y2 = k.feld2()

    d = abs(feld[y1][x1] - feld[y2][x2])
    if d < 1:
        diff += 1 - d

print(diff)
print(diff / bester_weg.kosten_ende)

''' Matrix optimal verändern '''

# Felder an allen Kanten entsprechend verändern
for a in bester_weg.abschnitte:
    # Bewegte Erde und Kante werden von jedem Abschnitt gepaart benutzt
    for i, k in zip(a.verschieben, a.kanten):
        x1, y1 = k.feld1()
        x2, y2 = k.feld2()

        # Bewegte Erde von Feld 1 abziehen und zu Feld 2 addieren
        feld[y1][x1] -= i
        feld[y2][x2] += i

''' Lösung ausgeben '''

ausgabe = open(datei + "-lsg.txt", "w")  # Ausgabedatei öffnen

zeichne(feld, datei + "-lsg.tif", bester_weg)  # Bild zeichnen

# Augabedatei schreiben
ausgabe.write("%d\n" % n)  # N ausgeben
for reihe in feld:
    for x in reihe:
        ausgabe.write("%.4f " % x)  # Zahl auf 4 Nachkommastellen ausgeben
    ausgabe.write("\n")