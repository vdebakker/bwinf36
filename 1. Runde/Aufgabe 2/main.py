from gruppe import *
from time import clock


def neueGruppe(alteGruppe, neue_karte):
    """
    Erstellt eine neue Gruppe, die eine alte Gruppe um eine Karte erweitert.
    Es werden die Anzahl an Personen sowie
    die Anzahl an Gutscheinen und Karten aktualisiert

    :param alteGruppe 'class': Die Gruppe, die um eine Karte erweitert wird
    :param neue_karte 'class': Mit dieser karte wird die Gruppe erweitert
    :return: 'class' neue Gruppe, die aus alter Gruppe und Karte gebildet wurde
    """
    name_karte = neue_karte.name  # Name der Karte
    # Aktualisierte Anzahl an Jugendlichen ohne Karte
    jugendlich = alteGruppe.jugendliche - neue_karte.jugendliche
    # Aktualisierte Anzahl an Erwachsenen ohne Karte
    erwachsene = alteGruppe.erwachsene - neue_karte.erwachsene

    # Anzahl an Gutscheinen wird aktualisiert
    gutscheine = alteGruppe.gutscheine
    if name_karte == "Gutschein":
        gutscheine -= 1

    # Dictionary mit Anzahl an Karten wird aktualisiert
    neue_karten = alteGruppe.karten.copy()
    neue_karten[name_karte] += 1  # Anzahl der gewählten Karte wird um 1 erhöht
    # Kosten werden aktualisiert
    neue_kosten = alteGruppe.eintrittskosten + preise[name_karte]
    return Gruppe(jugendlich, erwachsene, wochenende, schulzeit,
                  gutscheine, neue_karten, neue_kosten)

""" Input einlesen """

clock()
input = open("beispiel.txt").readlines()

# Anzahl an Kindern unter 4 Jahren
kinder = int(input[0].split(" ")[0])
# Anzahl an Jugendlichen unter 17 Jahren
jugendliche = int(input[1].split(" ")[0])
# Anzahl an Erwachsenen mit mindestens 17 Jahren
erwachsene = int(input[2].split(" ")[0])
# Anzahl an verfügbaren Gutscheinen
gutscheine = int(input[3].split(" ")[0])
# Wahrheitswerte für Schulzeit und Wochenende
schulzeit = input[4].split(" ")[0] == "True"
wochenende = input[5].split(" ")[0] == "True"

# Festlegen der Preise
preise = {"Jugendkarte": 2.5, "Erwachsenenkarte": 3.5, "Familienkarte": 8,
          "Tageskarte": 11, "Gutschein": 0}

# Berechnen der Wochentagrabatts für Einzelkarten
if not wochenende:
    preise["Jugendkarte"] *= .8
    preise["Erwachsenenkarte"] *= .8

# Dictionary mit Anzahl an Karten wird initialisiert
# Von jedem Typ gibt es zu Beginn 0 Karten
anfangs_karten = {karten_name: 0 for karten_name in preise}

""" Kontrollieren, ob der Eintritt möglich ist """

eintritt_moeglich = True  # Wahrheitswert, ob Eintritt möglich ist
if kinder > 0 and erwachsene == 0:  # Kinder vorhanden, aber keine Erwachsenen
    # Kinder dürfen nicht ohne Erwaxchsene in das Schwimmbad
    eintritt_moeglich = False

""" Alle möglichen Gruppen finden """

# Erste Gruppe mit Anfangskarten und den bisherigen Kosten von 0
# Anzahl an Jugendlichen, Erwachsenen, Gutscheinen und
# Wahrheitswerte für Schulzeit und Wochenende werden übergeben
erste_gruppe = Gruppe(jugendliche, erwachsene, wochenende, schulzeit,
                      gutscheine, anfangs_karten, 0)

# Liste mit Gruppen
# Am Anfang besteht diese nur aus der ersten Gruppe
gruppen = [erste_gruppe]

# Dictionary mit Gruppeninformation als Key und dazu gehörige Gruppe als Value
# Dieses Dictionary wird benötigt um zu testen,
# ob Gruppen bereits gefunden wurden und diese gegebenenfalls zu vergleichen
gruppen_informationen = {}
fertige_gruppen = []  # Liste mit Gruppen, in denen alle Personen Karten haben

# Es können noch Gruppen gefunden werden und der Eintritt ist möglich
while gruppen != [] and eintritt_moeglich:

    alte_gruppe = gruppen.pop()  # Alte Gruppe wird geladen

    if alte_gruppe.kartenVergeben():  # Alle Perspnen besitzen eine Karte
        fertige_gruppen.append(alte_gruppe)
    else:  # Nicht alle Personen besitzen eine Karte
        # Alle Karten, die als nächstes gewählt werden könnten,
        # werden aufgerufen
        for karte in alte_gruppe.moeglicheKarten():

            """ Erstellen neuer Gruppe """

            # Neue Gruppe wird erstellt
            neue_gruppe = neueGruppe(alte_gruppe, karte)
            # Informationen der neuen Gruppe werden geladen
            neue_info = neue_gruppe.info()
            # Gruppe mit selben Daten bereits gefunden
            if neue_info in gruppen_informationen.keys():
                # Andere Gruppe wird geladen
                andere_gruppe = gruppen_informationen[neue_info]
                # Wenn die Eintrittskosten der neuen Gruppe
                # niedriger sind als die Kosten der anderen
                # Gruppe wird die neue Gruppe hinzugefügt
                if neue_gruppe.eintrittskosten < \
                        andere_gruppe.eintrittskosten:
                    # Gruppe wird unter ihrer Information gespeichert,
                    # um zu erkennen, ob eine Gruppeinformation
                    # bereits einmal gefunden wurde
                    gruppen_informationen[neue_info] = neue_gruppe
                    # Gruppe mit höherem Eintrittspreis wird entfernt
                    gruppen.remove(andere_gruppe)
                    # Gruppe wird bei allen Gruppen hinzugefügt
                    gruppen.append(neue_gruppe)
            else:
                # Gruppe wird unter ihrer Information gespeichert,
                # um zu erkennen, ob eine Gruppeinformation bereits
                # einmal gefunden wurde
                gruppen_informationen[neue_info] = neue_gruppe
                # Gruppe wird bei allen Gruppen hinzugefügt
                gruppen.append(neue_gruppe)

""" Gefundene Gruppen auswerten """

# Gutscheinrabatt von 10% für eine Gruppe wird berechnet
for gruppe in fertige_gruppen:
    # Gutschein noch vorhanden und erlaubt
    if gruppe.gutscheine >= 1 and schulzeit:
        gruppe.gutscheine -= 1
        gruppe.karten["Gutschein"] += 1
        gruppe.eintrittskosten *= .9

output_datei = open("loesung.txt", "w")

if eintritt_moeglich and fertige_gruppen:

    # Günstigste Gruppe wird gesucht
    guenstigste_gruppe = fertige_gruppen[0]
    for gruppe in fertige_gruppen[1:]:
        if gruppe.eintrittskosten < guenstigste_gruppe.eintrittskosten:
            # Neue günstigste Gruppe gefunden
            guenstigste_gruppe = gruppe

    # Ergebnisse werden ausgegeben
    print("%.2f € für:" % guenstigste_gruppe.eintrittskosten,
          file=output_datei)
    for karten_typ, anzahl in guenstigste_gruppe.karten.items():
        print("%d x %s" % (anzahl, karten_typ), file=output_datei)

else:
    print("Eintritt nicht möglich", file=output_datei)

print("Zeit: %.4f s" % (clock()))
