from karte import *

class Gruppe:
    """
    Beschreibt die Besuchergruppe mit ihren Eintrittskarten.
    """

    def __init__(self, jugendliche, erwachsene, wochenende, schulzeit,
                 gutscheine, karten, kosten):
        # Anzahl an Jugendlichen, die noch keine Karte besitzen
        self.jugendliche = jugendliche
        # Anzahl an Erwachsenen, die noch keine Karte besitzen
        self.erwachsene = erwachsene
        # Anzahl an Personen, die noch keine Karte besitzen
        self.personen = jugendliche + erwachsene
        self.eintrittskosten = kosten  # Bisherige Summe der Preise der Karten
        # Anzahl an noch nicht verwendeten Gutscheinen
        self.gutscheine = gutscheine
        # Dictionary in dem die Anzahl der Karten gespeichert wird
        # Der Name der Karte ist dabei der Key und
        # die Anzahl an Karten von diesem Typ ist der Value
        self.karten = karten
        # Wahrheitswerte für Schulzeit und Wochenende
        self.__wochenende, self.__schulzeit = wochenende, schulzeit

    def moeglicheKarten(self):
        """
        Gibt mögliche Karten zurück, die als nächstes gewählt werden können.
        :return: 'list': Liste mit möglichen Karten
        """
        # Alle möglichen Karten werden zurückgegeben.
        # Dazu werden Listen mit Karten eines Typs addiert.
        return self.__jugendlicheKarten() + self.__erwachseneKarten() + \
               self.__familienKarten() + self.__gutscheinKarten() + \
               self.__tagesKarten()

    def __jugendlicheKarten(self):
        if self.jugendliche > 0:  # Es gibt noch Jugendliche ohne Karte
            return [Karte("Jugendkarte", 1, 0)]

        # Alle Jugendlichen haben Karten
        return []

    def __erwachseneKarten(self):
        if self.erwachsene > 0:  #Es gibt noch Erwachsene ohne Karte
            return [Karte("Erwachsenenkarte", 0, 1)]

        # Alle Erwachsenen haben Karten
        return []

    def __gutscheinKarten(self):
        if not self.__schulzeit:  # Gutscheine sind nicht gültig in den Ferien
            return []

        karten = []  # Liste mit Gutscheinkarten
        if self.gutscheine > 0:  # Gutscheine sind noch vorhanden
            if self.jugendliche > 0:
                # Es gibt noch Jugendliche ohne Karte, desshalb wird
                # eine Gutscheinkarte für einen Jugendlichen hinzugefügt
                karten.append(Karte("Gutschein", 1, 0))
            if self.erwachsene > 0:
                # Es gibt noch Erwachsene ohne Karte, desshalb wird
                # eine Gutscheinkarte für einen Erwachsenen hinzugefügt
                karten.append(Karte("Gutschein", 0, 1))

        return karten

    def __familienKarten(self):
        # Hinzufügen aller Konstellationen von Familienkarten

        karten = [] # Liste für Familienkarten
        # Karten mit ein bzw. zwei Jugendlichen und
        # zwei Erwachsenen werden hinzugefügt
        for jugendliche in [1, 2]:
            karten.append(Karte("Familienkarte", jugendliche, 2))
        # Karten mit zwei bzw. drei Jugendlichen und
        # einem Erwachsenen werden hinzugefügt
        for jugendliche in [3, 2]:
            karten.append(Karte("Familienkarte", jugendliche, 1))

        # Löschen der Karten, die nicht möglich sind
        for karte in karten.copy():
            if karte.jugendliche > self.jugendliche or \
                            karte.erwachsene > self.erwachsene:
                # Nicht genügend Jugendliche oder Erwachsene ohne Karte
                # Die Karte ist für zu viele Jugendliche
                # oder Erwachsene ausgelegt
                karten.remove(karte)

        return karten

    def __tagesKarten(self):
        if self.__wochenende:  # Keine Tageskarten erlaubt
            return []

        if self.personen < 4:  # Keine Tageskarte sinnvoll
            return []

        karten = []  # Liste für Tageskarten

        # Maximale Anzahl an Jugendlichen,
        # die mit einer Tageskarte in das Schwimmbad können
        # Bei z.B. 8 Jugendlichen wäre dieser Wert 6,
        # bei 4 Jugendlichen wäre er 4
        jugend_max = min(6, self.jugendliche)

        # Jede mögliche Anzahl an Jugendlichen ,
        # die in das Schwimmbad kann wird aufgerufen
        for jugendliche in range(jugend_max + 1):
            # Anzahl an Erwachsene, die in das Schwimmbad kann, wird berechnet
            erwachsene = min(6 - jugendliche, self.erwachsene)
            if jugendliche + erwachsene > 3:  # Tageskarte ist sinnvoll
                # neue Tageskarte wird hinzugefügt
                karten.append(Karte("Tageskarte", jugendliche, erwachsene))

        return karten

    def kartenVergeben(self):
        # Bei 0 Personen ohne Karte sind alle Karten vergeben
        return self.personen == 0

    def info(self):
        # Wichtigste Daten der Gruppe werden zurückgegeben
        # Mit diesen Daten können zwei Gruppe verglichen werden
        # Sie werden als identisch angesehen,
        # falls deren info-Werte gleich sind
        return self.jugendliche, self.erwachsene, self.gutscheine
