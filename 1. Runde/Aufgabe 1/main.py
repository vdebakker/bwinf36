from person import *
from time import clock


def finde_person(name, schulklasse):
    """
    Identifiziert person aus "schulklasse" mit dem attribut "name"
    
    :param name: 'str': hier: der Name einer einzelnen Schülerin
    :param schulklasse: 'set': hier: Gruppe von Schülerinnen
    :return: person: 'class'
    """

    for person in schulklasse:
        if person.name == name:
            return person


def notwendige_personen(person, nicht_zugeordnete_schuellerinnen):
    """
    Identifiziert alle Schülerinnen,
    die mit der übergebenen person ein Zimmer teilen wollen

    :param person: 'class': ausgewählte Schülerin
    :param nicht_zugeordnete_schuellerinnen: 'set': Schülerinnen,
     die noch auf Zimmer aufgeteilt wurden
    :return: 'set': alle Schülerinnen,
    die mit der übergebenen person ein Zimmer teilen müssen
    """

    personen = set()

    # Alle Wunschpersonen von 'person' werden hinzugefügt
    for wunsch_name in person.teilen:
        # Identifizierung Wunschperson
        wunsch_person = finde_person(wunsch_name,
                                     nicht_zugeordnete_schuellerinnen)
        if wunsch_person:  # Person gefunden
            personen.add(wunsch_person)  # Gewünschte Person wird hinzugefügt

    # Alle Personen werden hinzugefügt, die 'person' als Wunschperson haben
    for schuelerin in nicht_zugeordnete_schuellerinnen:
        if person.name in schuelerin.teilen:  # 'person' ist Wunschperson?
            personen.add(schuelerin)  # identifizierte Person wird hinzugefügt

    return personen


def zimmer(person, nicht_zugeordnete_schuellerinnen):
    """
    Stellt Zimmerbelegung mit Wunschpersonen zusammen

    :param person: 'class': Ausgangsperson für Zimmerbelegung
    :param nicht_zugeordnete_schuellerinnen: 'set':
    Schülerinnen, die noch auf Zimmer aufgeteilt wurden
    :return: 'list': alle Personen, die ein Zimmer belegen
    """

    list_personen = [person]  # Initialisierung mit Ausgangsperson

    i = 0
    while i < len(list_personen):

        # Aufbau der Zimmerbelegung mit Wunschpersonen
        for person in notwendige_personen(list_personen[i],
                                          nicht_zugeordnete_schuellerinnen):
            if person not in list_personen:  # Personen noch nicht im Zimmer
                list_personen.append(person)

        i += 1

    return list_personen


def verstoss(zimmer):
    """
    Überprüft, ob Zimmerbelegung gegen den Wunsch verstösst,
    nicht mit bestimmter anderer Person ein Zimmer zu teilen

    :param zimmer: zu untersuchende Zimmerbelegung
    :return:    True: Verstoss gegen gewünschte Zimmerbelegung
                False: sonst
    """

    # Alle Namen der Personen im Zimmer
    namen_zimmer = {person.name for person in zimmer}
    for person in zimmer:
        # Vergleich der Ablehnungswünsche der Personen
        # im Zimmer mit aktueller Zimmerbelegung
        if person.nicht_teilen & namen_zimmer:
            return True
    return False


""" Initialisierung """

clock()

# Initialisierung der Variablen

schulklasse = set()  # Set mit allen Schülerinnen der Klasse 9c,
# die auf die Zimmer aufgeteilt werden sollen
zugeordnete_schuellerinnen = set()  # Set mit allen Schülerinnen,
# die schon einem Zimmer zugeordnet wurden
zimmerbelegungen = []  # Liste mit Zimmerbelegungen
# Wahrheitswert, ob ein Belegungswunsch nicht erfüllt
# werden kann (Initial: kein Verstoß)
verstoesse = False

""" Einlesen der Input-Datei """

input_list = open("zimmerbelegung.txt").readlines()

for i in range(0, len(input_list), 4):
    name = input_list[i].strip()  # name der Schülerin
    # Listen mit Personen, mit denen die Schülerin
    # das Zimmer teilen bzw. nicht teilen möchte
    teilen = input_list[i + 1].split()[1:]
    nicht_teilen = input_list[i + 2].split()[1:]

    # Ergänzung um eingelesene Schülerinnen
    schulklasse.add(Person(name, set(teilen), set(nicht_teilen)))


""" Schülerinnen auf Zimmer aufteilen """

# Berücksichtigung nur der positiven Belegungswünsche

for person in schulklasse:
    # Person wurde noch nicht einem Zimmer zugeordnet
    if person not in zugeordnete_schuellerinnen:
        # Neues Zimmer wird erstellt
        neues_zimmer = zimmer(person, schulklasse - zugeordnete_schuellerinnen)

        # Die zugeordneten Personen werden um
        # die Personon des neuen Zimmers erweitert
        zugeordnete_schuellerinnen |= set(neues_zimmer)
        # Die bisheringen Zimmerbelegugen werden um das neue Zimmer ergänzt
        zimmerbelegungen.append(neues_zimmer)


""" Ergebnis ausgeben und in Datei schreiben """

output_datei = open("zimmeraufteilung.txt", "w")  # Output datei

# Ausgabe, falls Belegung nicht den Wünschen entspricht
for zimmer in zimmerbelegungen:
    if verstoss(zimmer):  # Zimmer nicht möglich
        verstoesse = True
        print("Das Zimmer mit der Belegung:", *zimmer
              , "entspricht nicht den Wünschen der Schülerinnen",
              file=output_datei)

if not verstoesse:  # Zimmeraufteilung möglich
    print("Aufteilung möglich")

    for i, zimmer in enumerate(zimmerbelegungen):
        print("%d. Zimmer: " % (i + 1), end="", file=output_datei)
        print(*zimmer, sep=", ", file=output_datei)

print("Zeit: %.4f s" % (clock()))
