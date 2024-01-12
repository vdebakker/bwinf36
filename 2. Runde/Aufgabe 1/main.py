from reihe import Reihe
from mauer import Mauer

def rahmen(luecken, anzahl_reihen, verfuegbare_bloecke):
    """ Erstellt Rahmen (Reihen ohne Blöcke) für Mauer.
    Der Rahmen muss im folgenden Schritten mit Blöcken gefüllt werden.
    
    :param luecken: Anzahl an erlaubten Stellen ohne Fuge in der Mauer (für
    Erweiterung)
    :param anzahl_reihen: Anzahl an Reihen, die die Mauer haben soll
    :param verfuegbare_bloecke: Blöcke, die für jede Reihe verfügbar sind.
    Bei ungeraden n wird der längste Block vorerst ignoriert. Er wird am
    Ende in die mit n-1 Blöcken erstellte Mauer eingefügt.
    :return: Mauer mit Reihen ohne Blöcke
    """

    # Anfangsmauer wird erstellt
    mauer = Mauer(luecken)

    # Leere Reihen werden zur Mauer hinzugefügt
    for j in range(anzahl_reihen):
        # Leere linke Reihe wird erstellt
        r_links = Reihe(j, [], verfuegbare_bloecke.copy())

        # Leere rechte Reihe mit gleichen verfügbaren Blöcken wird erstellt
        r_rechts = Reihe(j, [], r_links.verfuegbar)
        mauer.reihen_links.append(r_links)
        mauer.reihen_rechts.append(r_rechts)

    return mauer


def mauer_bauen(mauer, pos, seite, mitte, selbe_verfuegbar):
    """ Baut eine Mauer auf, indem versucht wird, einen Block einer Reihe so
    hinzuzufügen, sodass an der übergebenen Position eine Fuge entsteht.
    Wenn dies möglich ist, wird versucht an der nächsten freien Position eine
    Fuge entstehen zu lassen, indem die Funktion sich selbst aufruft.
    Es werden abwechselnd an der linken und rechten Seite der Mauer Steine
    hinzugefügt.
    Falls bei keiner Reihe ein Stein hinzugefügt werden kann, kann eine
    Lücke gelassen werden, wenn die Mauer das erlaubt (nur bei Erweiterung).
    :param mauer: Mauer, die versucht wird zu erweitern
    :param pos: Position, an der eine Fuge entstehen soll
    :param seite: Seite, auf der ein Block hinzugefügt werden soll
    :param mitte: Mitte der Mauer. Wenn die Position erreicht wird,
    kann die Suche beendet werden
    :param selbe_verfuegbar: Wahrheitswert, ob alle Reihen die verfügbaren
    Blöcke teilen
    :return: Fertige Mauer, falls diese gefunden wurde. Sonst wird nichts
    zurückgegeben.
    """

    # Prüfung, ob Ende des Mauerbaus erreicht wurde
    if pos > mitte or (pos == mitte and seite == "rechts"):
        # Erweiterung 2: Da die Reihen ggfs. mit unterschiedlichen Reihen gefüllt
        # werden, muss überprüft werden, ob am Ende der Analyse die noch zu
        # füllenden Lücken durch die noch verfügbaren Blöcke geschlossen
        # werden können.
        if selbe_verfuegbar:  # gilt für Erweiterung 2

            mauer.sortiere()  # Reihen in der Mauer werden sortiert
            # Liste, in der die verwendeten Blöcke gespeichert werden
            verwendet = []
            for reihe_links, reihe_rechts in zip(mauer.reihen_links,
                                                 mauer.reihen_rechts):
                # Benötigter Block, um die Lücke zu füllen
                benoetigt = mitte * 2 - sum(reihe_links.bloecke) - sum(
                    reihe_rechts.bloecke)
                # Es wird überprüft, ob der benötigte Block noch vorhanden ist
                if benoetigt in reihe_links.verfuegbar:
                    # Der benötigte Block ist noch vorhanden, wird von den
                    # verfügbaren Blöcken gelöscht und den verwendeten
                    # Blöcken angehängt
                    reihe_links.verfuegbar.remove(benoetigt)
                    verwendet.append(benoetigt)
                else:
                    # Der benötigte Block ist nicht vorhanden
                    # Die Reihen werden in die ursprüngliche Reihenfolge
                    # gebracht.
                    mauer.reihen_links = sorted(mauer.reihen_links,
                                                key=lambda x: x.ende)
                    mauer.reihen_rechts = sorted(mauer.reihen_rechts,
                                                 key=lambda x: x.ende)
                    # Änderungen an den verfuegbaren Blöcen werden
                    # rückgängig gemacht
                    reihe_links.verfuegbar.extend(verwendet)
                    # Es wird None zurückgegeben, da dies keine gültige
                    # Lösung ist
                    return None
            # Alle benötigten Blöcke waren noch vorhanden, eine Lösung ist
            # gefunden und den verfügbaren Blöcke werden wieder die
            # verwendeten Blöcke zurückgegeben
            mauer.reihen_links[0].verfuegbar.extend(verwendet)
        return mauer

    # Die richtige Liste mit Reihen wird identifiziert. Wenn die linke Seite
    # erweitert werden soll, sind das die Reihen der linken Seite,
    # rechts analog.
    reihen = mauer.reihen_links if seite == "links" else mauer.reihen_rechts

    # Alle Reihen und ihre Position in der Mauer werden aufgerufen
    for i, reihe in enumerate(reihen):

        # Nächster notwendiger Block wird berechnet
        # Er wird so gewählt, dass die nächste Fuge erreicht werden würde
        notwendig = pos - reihe.ende

        # Notwendiger Block ist noch verfügbar, wurde noch nicht gewählt und
        # kann desshalb der Reihe angehängt werden
        if notwendig in reihe.verfuegbar:

            ''' Notwendige Änderungen werden vollzogen '''

            # Notwendiger Block wird der Reihe angehängt
            reihe.bloecke.append(notwendig)

            # Gewählter Block wird aus verfügbaren Blöcken entfernt
            reihe.verfuegbar.remove(notwendig)

            reihe.ende += notwendig  # Ende der Reihe wird aktualisiert

            # Laengster Block wird aktualisiert, falls nötig
            if reihe.laengster == notwendig and len(reihe.verfuegbar) != 0:
                reihe.laengster = max(reihe.verfuegbar)

            # Reihe wird aus Mauer entfernt und ans Ende wieder angehängt,
            # um weiterhin eine Sortierung der Reihen zu erreichen
            del reihen[i]
            reihen.append(reihe)

            # Es wird weiter nach einer Mauer gesucht.
            # Dazu wird als Position die nächste Fuge übergeben
            if seite == "links":
                # An der selben Stelle auf der rechten Seite wird weiter gesucht
                potenzielle_mauer = mauer_bauen(mauer, pos, "rechts", mitte,
                                                selbe_verfuegbar)
            else:
                # Eine Position weiter auf der linken Seite wird weiter gesucht
                potenzielle_mauer = mauer_bauen(mauer, pos + 1, "links",
                                                mitte, selbe_verfuegbar)

            # Wenn eine Mauer gefunden wurde, wird diese zurückgegeben
            if potenzielle_mauer: return potenzielle_mauer

            ''' Änderungen werden rückgängig gemacht '''

            # Änderungen werden rückgängig gemacht, da keine Mauer gefunden
            # wurde

            # Letzter Block wird entfernt
            del reihe.bloecke[-1]

            # Notwendiger Block wird wieder den verfügbaren Blöcken hinzugefügt
            if type(reihe.verfuegbar) == set:
                reihe.verfuegbar.add(notwendig)
            else:
                reihe.verfuegbar.append(notwendig)

            # Ende wird aktualisiert
            reihe.ende -= notwendig

            # Längster Block wird aktualisiert, falls nötig
            if notwendig > reihe.laengster: reihe.laengster = notwendig

            # Reihe wird wieder an ursprüngliche Position in der Reihe eingefügt
            del reihen[-1]
            reihen.insert(i, reihe)

        # Wenn der notwendige Block länger als der längste Block
        # in der Reihe ist, kann die Suche abgebrochen werden
        elif notwendig > reihe.laengster:
            return None

    # Erweiterung 1 & 2: Wenn noch Lücken erlaubt sind, kann diese Fuge
    # ausgelassen werden
    if mauer.max_luecken > 0:

        # Anzahl an Lücken wird aktualisiert
        mauer.max_luecken -= 1

        # Es wird weiter nach einer Mauer gesucht
        # Dazu wird als Position die nächste Fuge übergeben
        if seite == "links":
            # An der selben Stelle auf der rechten Seite wird weiter gesucht
            potenzielle_mauer = mauer_bauen(mauer, pos, "rechts", mitte,
                                            selbe_verfuegbar)
        else:
            # Eine Position weiter auf der linken Seite wird weiter gesucht
            potenzielle_mauer = mauer_bauen(mauer, pos + 1, "links", mitte,
                                            selbe_verfuegbar)

        # Wenn eine Mauer gefunden wurde, wird diese zurückgegeben
        if potenzielle_mauer: return potenzielle_mauer

        # Änderung wird rückgängig gemacht
        mauer.max_luecken += 1

    # Keine Mauer wurde gefunden und nichts wird zurückgegeben
    return None


''' Hauptaufgabe: Mauern für vorgegebene n berechnen '''

# Datei, in der die vorgegebenen n stehen
datei_n = open("n.txt", "r").readlines()[1:]
liste_n = [int(n) for n in datei_n]  # Liste mit n



for n in liste_n:
    # Basis-Blöcke werden erstellt
    # Bei ungeraden Zahlen werden nur die Blöcke bis n - 1 betrachtet.
    # Am Ende kann der letzte Block pro Reihe leicht eingefügt werden
    if n % 2 == 0:
        basis_bloecke = list(range(1, n + 1))
    else:
        basis_bloecke = list(range(1, n))

    mitte = sum(basis_bloecke) / 2  # Mitte wird bestimmt
    # Höhe der Mauer und gleichzeitig Anzahl an Reihen in der Mauer
    hoehe = n // 2 + 1
    # Anfängliche Mauer wird gebaut:
    anfangs_mauer = rahmen(0, hoehe, set(basis_bloecke))

    if n > 1:
        # Mauer besteht aus mehreren Steinen und muss gebaut werden
        mauer = mauer_bauen(anfangs_mauer, 1, "links", mitte, False)
    else:
        # Mauer besteht aus 1 oder 0 Steinen und muss nicht gebaut werden
        mauer = anfangs_mauer

    mauer.letzte_bloecke_hinzufuegen(n)  # Letzte Blöcke werden hinzugefügt

    mauer.sortiere()  # Reihen in der Mauer werden sortiert

    # Mauer wird gezeichnet und geschrieben
    mauer.zeichne("n%d.tif" % n)
    mauer.schreibe("n%d.txt" % n)



''' Erweiterung 1: Mauer mit vorgegebenen Blöcken für jede Reihe berechnen '''

# Datei, in der die vorgegebenen Blöcke stehen
datei_bloecke = open("erweiterung1.txt", "r").readlines()[1:]
bloecke = [int(n) for n in datei_bloecke]   # Liste mit Längen der Blöcke


# Anfängliche Mauer wird als None deklariert, damit die while-Schleife
# abbrechen kann, falls sie nicht mehr als None geflagt wird
mauer = None

breite = sum(bloecke)  # Breite der Mauer
fugen_pro_reihe = len(bloecke) - 1  # Fugen pro Reihe
max_fugen_gesamt = breite - 1  # Maximale Anzahl an Fugen
mitte = breite / 2

# Höhe der Mauer und gleichzeitig Anzahl an Reihen in der Mauer sind begrenzt
# durch die maximale Anzahl an Fugen und die Anzahl an Blöcken
hoehe = max_fugen_gesamt // fugen_pro_reihe
if hoehe > len(bloecke):
    # Jede Reihe muss mit einem unterschiedlichen Stein anfangen,
    # desshalb gibt es höchstens so viele Reihen wie Steine
    hoehe = len(bloecke)

# Mauer wird gesucht, solange keine gefunden wurde
while not mauer:
    # Anzahl an erlaubten Lücken wird berechnet
    luecken = max_fugen_gesamt - hoehe * fugen_pro_reihe

    # rahmen wird erstellt
    anfangs_mauer = rahmen(luecken, hoehe, bloecke)

    # Mauer wird versucht zu bauen
    mauer = mauer_bauen(anfangs_mauer, 1, "links", mitte, False)

    # Anzahl an Reihen wird vermindert
    hoehe -= 1

mauer.letzte_bloecke_hinzufuegen()  # Letzte Blöcke werden hinzugefügt

mauer.sortiere()  # Reihen in der Mauer werden sortiert

mauer.zeichne("erweiterung1_lsg.tif")  # Mauer wird gezeichnet und geschrieben
mauer.schreibe("erweiterung1_lsg.txt")


''' Erweiterung 2: Mauer für vorgegebene Blöcke berechnen '''

# Datei, in der die vorgegebenen Blöcke stehen
datei_bloecke = open("erweiterung2.txt", "r").readlines()[1:]
bloecke = [int(n) for n in datei_bloecke]  # Liste mit Längen der Blöcke

# Anfängliche Mauer wird als None deklariert, damit die while-Schleife
# abbrechen kann, falls sie nicht mehr als None geflagt wird
mauer = None

# Summe der Blöcke und gleichzeitig Summe der Längen der Reihen in der Mauer
# Damit können die möglichen Höhen der Mauer berechnet werden
summe = sum(bloecke)

# Teiler werden bestimmt. Das sind alle möglichen Höhen der Mauer,
# damit alle Reihen gleich lang sein können
teiler = []
for i in range(1, summe + 1):
    if summe % i == 0:
        teiler.append(i)

# Am Anfang wird der letzte Index gewählt, damit die größten Höhen zuerst
# ausprobiert werden
i = len(teiler) - 1

# Mauer wird gesucht, solange keine gefunden wurde
while not mauer:
    hoehe = teiler[i]  # Höhe der Mauer und gleichzeitig Anzahl an Reihen
    breite = summe // hoehe  # Breite der Mauer
    max_fugen_gesamt = breite - 1  # Maximale Anzahl an Fugen
    mitte = breite / 2

    # Anzahl an erlaubten Lücken wird berechnet
    luecken = max_fugen_gesamt - (len(bloecke) - hoehe)

    # Temporäre Liste für Blöcke wird erstellt, damit ursprüngliche Liste
    # nicht verändet wird
    tmp = bloecke[:]

    # Mauer mit übergebener Anzahl an Lücken wird erstellt
    anfangs_mauer = Mauer(luecken)

    # Leere Reihen werden zur Mauer hinzugefügt. Alle Reihen haben die
    # gleichen verfügbaren Blöcke
    for j in range(hoehe):
        # Leere linke und rehcte Reihen werden erstellt
        r_links = Reihe(j, [], tmp)
        r_rechts = Reihe(j, [], tmp)
        anfangs_mauer.reihen_links.append(r_links)
        anfangs_mauer.reihen_rechts.append(r_rechts)

    print(hoehe)

    # Mauer wird versucht zu bauen
    mauer = mauer_bauen(anfangs_mauer, 1, "links", mitte, True)
    i -= 1

mauer.sortiere()  # Reihen in der Mauer werden sortiert

# Letzte Blöcke werden hinzugefügt
for reihe_links, reihe_rechts in zip(mauer.reihen_links, mauer.reihen_rechts):
    # Benötigter Block wird so berechnet, damit die Lücke zwischen der
    # linken und der rechten Reihe gefüllt wird
    benoetigt = breite - sum(reihe_links.bloecke) - sum(reihe_rechts.bloecke)
    print(benoetigt)
    # Fehlender letzter Block wird hinten an linke Liste angehängt.
    reihe_links.bloecke.append(benoetigt)
    reihe_links.verfuegbar.remove(benoetigt)

mauer.zeichne("erweiterung2_lsg.tif")  # Mauer wird gezeichnet und geschrieben
mauer.schreibe("erweiterung2_lsg.txt")