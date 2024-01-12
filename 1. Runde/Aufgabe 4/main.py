from kennzeichen import *
from kennzeichenfolge import *
from time import clock


def potenzielle_kuerzel(wort):
    """
    Findet alle Kürzel für ein übergebenes Wort.
    Kürzel müssen ein bis drei Buchstaben lang
    und in der Kürzelliste enthalten sein
    
    :param wort: 'str': Wort, das mit Kennzeichen geschrieben werden soll
    :return: 'list': Liste mit möglichen Kürzeln
    """

    # Liste mit möglichen Kürzeln. Sie werden aus ein bis drei
    # der ersten Buchstaben des Wortes gebildet
    moegliche_kuerzel = [wort[:1], wort[:2], wort[:3]]

    # Löschen von Kürzeln, die nicht in Kürzelliste enthalten sind
    # und somit kein Stadtküzel sind
    for kuerzel in moegliche_kuerzel[:]:
        if kuerzel not in alle_kuerzel:  # Nicht in Kürzelliste enthalten
            moegliche_kuerzel.remove(kuerzel)

    return moegliche_kuerzel


def potenzielle_buchstaben(wort):
    """
    Findet alle Buchstabenkombinationen, die dem Kürzel folgen könnten.
    Diese müssen ein bis zwei Buchstaben lang sein,
    dürfen keine Umlaute enthalten und sind frei wählbar.
    
    :param wort: 'str': Wort, das mit Kennzeichen geschrieben werden soll
    :return: 'list': mögliche Buchstaben
    """

    buchstaben = []  # Liste mit Buchstabenkombinationen
    if len(wort) >= 1 and wort[0] not in "ÄÖÜ":
        # erster Buchstabe enthält keinen Umlaut

        # Buchstabenkombination mit erstem Buchstaben wird hinzugefügt
        buchstaben.append(wort[:1])
        if len(wort) >= 2 and wort[1] not in "ÄÖÜ":
            # zweiter Buchstabe enthält keinen Umlaut

            # Buchstabenkombination mit
            # ersten beiden Buchstaben wird hinzugefügt
            buchstaben.append(wort[:2])

    return buchstaben


def potenzielle_kennzeichen(wort):
    """
    Findet alle Kennzeichen für übergebenes Wort.
    Sie setzen sich aus Stadtkürzel und Buchstabenkombination zusammen.
    
    :param wort: 'str': Wort, das mit Kennzeichen geschrieben werden soll
    :return: Liste mit möglichen Kennzeichen
    """
    
    moegliche_kennzeichen = []  # Liste mit möglichen Kennzeichen
    # Alle möglichen Kürzel werden aufgerufen
    for kuerzel in potenzielle_kuerzel(wort):
        # Restliches wort wird berechnet, um Buchstabenkombinationen zu finden
        rest_wort_kuerzel = wort[len(kuerzel):]
        #  Alle möglichen Buchstabenkombinationen werden aufgerufen
        for buchstaben in potenzielle_buchstaben(rest_wort_kuerzel):
            # Neues Kennzeichen wird hinzugefügt
            moegliche_kennzeichen.append(Kennzeichen(kuerzel, buchstaben))

    return moegliche_kennzeichen


def kennzeichen_ganzes_wort(wort):
    """
    Findet alle Kennzeichen, die ein gesamtes Wort abbilden.
    :param wort: 'str': Wort, das mit Kennzeichen geschrieben werden soll
    :return: Liste mit möglichen Kennzeichen
    """

    # Liste mit möglichen Kennzeichen
    kennzeichen = potenzielle_kennzeichen(wort)
    for k in kennzeichen[:]:
        if len(k) < len(wort):  # Kennzeichen bildet nicht gesamtes Wort ab
            kennzeichen.remove(k)

    return kennzeichen


''' Input einlesen '''

clock()

kuerzelliste = open("kuerzelliste.txt").readlines()  # Liste mit Kürzeln
# Set mit Kürzeln
alle_kuerzel = frozenset(kuerzel.strip() for kuerzel in kuerzelliste)
output_datei = open("loesung.txt", "w")


""" Teilaufgabe 1: Testen, ob TIMO mit Kennzeichen geschrieben werden kann """

# Liste mit Kennzeichen, die TIMO komplett abbilden
kennzeichen = kennzeichen_ganzes_wort("TIMO")
if kennzeichen:  # Kennzeichen für TIMO gefunden
    print("TIMO ist möglich, ", kennzeichen[0], file=output_datei)
else:  # Keine Kennzeichen gefunden
    print("TIMO ist nicht möglich", file=output_datei)
print(file=output_datei)


''' Teilaufgabe 2: Wörter ohne Kennzeichen finden '''

# Liste mit Wörtern, die nicht mit einem Kennzeichen geschrieben werden können
unmoegliche_woerter = []
max_anzahl_zu_suchender_woerter = 10

# Dateien mit Wörtern mit zwei, drei und vier
# Buchstaben werden nacheinander geöffnet
for i, datei in enumerate(("4buchstaben.txt", "3buchstaben.txt",
                           "2buchstaben.txt")):
    # Neue Liste wird hinzugefügt für Wörter mit n Buchstaben
    unmoegliche_woerter.append([])
    # Datei mit Wörtern mit n Buchstaben wird geöffnet
    woerter_list = open(datei).readlines()
    # Wörter mit n Buchstaben werden in Liste geholt
    woerter = [wort.strip() for wort in woerter_list]

    for w in woerter:  # Jedes Wort mit n Buchstaben wird aufgerufen
        # Liste mit Kennzeichen, die Woprt 'w' komplett abbilden
        kennzeichen = kennzeichen_ganzes_wort(w)
        if not kennzeichen:  # Keine Kennzeichen für Wort 'w' gefunden
            unmoegliche_woerter[i].append(w)
            # Bei zehn gefundenen Wörtern für n Buchstaben wird
            # nicht weiter nach Wörtern mit n Buchstaben gesucht
            if len(unmoegliche_woerter[i]) == max_anzahl_zu_suchender_woerter:
                break

print("Unmögliche Wörter:", file=output_datei)
for woerter in unmoegliche_woerter:
    print(*woerter, file=output_datei)
print(file=output_datei)


''' Teilaufgaben 3, 4: Kennzeichenfolgen finden '''

# Datei mit Wörtern, die mit Kennzeichen geschrieben werden sollen
wort_datei = open("autoscrabble.txt").readlines()
for wort in wort_datei:  # Jedes Wort wird aufgerufen
    wort = wort.strip()  # \n wird vom Wort entfernt

    # Liste mit Kennzeichenfolgen wird erstellt.
    # Zu Beginn gibt es eine Kennzeichenfolge mit leerer Liste für Kennzeichen.
    # Das restliche Wort besteht aus dem gesamten Wort,
    # da noch nichts vom Ausgangswort dargestllt wurde.
    kennzeichen_folgen = [KennzeichenFolge([], wort)]
    fertige_kennzeichenfolge = None  # Variable für fertige Kennzeichenfolge
    gefundene_woerter = set()  # Set mit allen bereits gebildeten Wörtern

    ''' Jede Kennzeichenfolge wird versucht, um Kennzeichen zu erweitern '''

    while kennzeichen_folgen != [] and fertige_kennzeichenfolge is None:
        # Noch nicht alle Kennzeichenfolgen in der Liste aufgerufen

        # Momentane Kennzeichenfolge, die versucht wird
        # um neue Kennzeichen zu erweitern
        kf = kennzeichen_folgen.pop()

        # Neue Kennzeichen für Kennzeichenfolge werden aufgerufen
        # Diese können der momentanen Kennzeichenfolge angehängt werden
        for neues_kennzeichen in potenzielle_kennzeichen(kf.rest_wort):
            # Neues restliche Wort wird berechnet
            # Dem restlichen Wort der Kennzeichenfolge
            # werden vorne die Buchstaben abgeschnitten,
            # die vom neuen Kennzeichen dargestellt werden
            neues_rest_wort = kf.rest_wort[len(neues_kennzeichen):]

            # Es wird überprüft,
            # ob das neue restliche Wort bereits gefunden wurde.
            # In diesem Fall muss es nicht weiter verfolgt werde
            if neues_rest_wort not in gefundene_woerter:
                # Wort noch nicht gefunden

                # Neue Kennzeichenfolgem wird erstellt
                # Die Liste mit Kennzeichen der alten Kennzeichenfolge wird
                # um das neue Kennzeichen erweitert und
                # das aktualisierte Wort wird übergeben
                neues_kennzeichenfolge = KennzeichenFolge(
                    kf.kennzeichen_list + [neues_kennzeichen], neues_rest_wort)

                if neues_kennzeichenfolge.fertig():
                    # Fertige Kennzeichenfolge gefunden

                    fertige_kennzeichenfolge = neues_kennzeichenfolge
                    # Es muss nicht weiter nach Kennzeichenfolgen gesucht werden
                    break

                else:
                    # Neue Kennzeichenfolge wird
                    # der Liste mit Kennzeichenfolgen angehängt
                    kennzeichen_folgen.append(neues_kennzeichenfolge)

                    # Neues restliche Wort wird Set mit gefundenen Wörtern
                    # hinzugefügt, damit es nicht mehrfach gezählt wird
                    gefundene_woerter.add(neues_rest_wort)

    ''' Ergebnis ausgeben '''

    print(wort + ":", file=output_datei)

    if fertige_kennzeichenfolge:
        print("Kennzeichenfolge gefunden", file=output_datei)
        print(*fertige_kennzeichenfolge.kennzeichen_list, sep=", ",
              file=output_datei)
    else:
        print("Kennzeichenfolge nicht gefunden", file=output_datei)
    print(file=output_datei)

print("Zeit: %.4f s" % (clock()))
