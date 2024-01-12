from kante import Kante
from kosten import optimum, abs_summe
from wegabschnitt import Abschnitt


class Weg:
    """ Stellt einen Weg dar und merkt sich dabei die Kanten, das Ende,
    alle Abschnitte des Weges, alle besuchten Punkte, die bisher benötigten
    Kosten und die Kosten, die mindestens bis zum Ende benötigt werden.
    Aus einem Weg können die möglichen nächsten Wege erstellt werden,
    die aus den möglichen nächsten Punkten und dem bisherigen Weg bestehen.
    """

    def __init__(self, kanten, ende, kosten, besuchte_punkte, abschnitte,
                 kosten_ende):
        self.kanten = kanten  # Liste mit gewählten Kanten
        self.ende = ende  # Endpunkt des Weges
        self.kosten = kosten  # Bisher benötigte Kosten
        self.besuchte_punkte = besuchte_punkte  # Set mit bisher besuchten
        # Punkten
        self.abschnitte = abschnitte  # Liste mit Abschnitten des Weges
        self.kosten_ende = kosten_ende  # Mindestens benötigte Kosten bis zum
        # Ende

    def copy(self):
        # Erstellt eine tiefe Kopie dieses Weges
        return Weg(self.kanten[:], self.ende, self.kosten,
                   self.besuchte_punkte.copy(),
                   [a.copy() for a in self.abschnitte], self.kosten_ende)

    def naechste_punkte(self, n):
        """ Liefert alle möglichen nächsten Punkte. Das sind alle
        benachbarten Punkte vom Ende des Weges, die innerhalb des Feldes
        liegen, noch nicht besucht wurden und zu denen eine Kante gebildet
        werden kann.
        :param n: Vorgegebenes n (Länge und Breite des Feldes)
        :return: Mögliche nächste Punkten als Generator
        """
        x, y = self.ende  # X- und Y- Koordinaten des Endes

        # Mögliche nächste Punkte
        punkte = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
        for punkt in punkte:
            # Punkt bereits besucht
            bereits_besucht = punkt in self.besuchte_punkte

            # Punkt nicht im Feld
            nicht_im_feld = not (0 <= punkt[0] <= n and 0 <= punkt[1] <= n)

            # Kante nicht erlaubt, da sie auf dem rechten oder linken Rand
            # liegen würde
            kante_rand_rl = x in [0, n] and punkt[0] in [0, n]

            # Kante nicht erlaubt, da sie auf dem oberen oder unteren Rand
            # liegen würde
            kante_rand_ou = y in [0, n] and punkt[1] in [0, n]
            if not(bereits_besucht or nicht_im_feld or
                    kante_rand_rl or kante_rand_ou):
                yield punkt

    def naechste_wege(self, n, matrix, lookup, min_ende):
        """ Liefert alle möglichen nächsten Wege.
        Diese werden aus den möglichen nächsten Punkten und dem bisherigen
        Weg gebildet.
        :param n: Vorgegebenes n (Länge und Breite des Feldes)
        :param matrix: Matrix mit Höhen der Planquadrate
        :param lookup: Lookup Liste mit schon berechneten Abschnitten
        :param min_ende: Liste mit Kosten, die noch mindestens bis zum Ende
        benötigt werden
        :return: Nächste Wege als Generator
        """

        punkte = self.naechste_punkte(n)  # Mögliche nächste Punkte
        # Für jeden Punkt wird ein Weg erstellt
        for neues_ende in punkte:
            neuer_weg = self.copy()  # Neuer Weg ist Kopie des alten Wegs
            neuer_weg.ende = neues_ende  # Neues Ende
            # Altes Ende wird zu besuchten Punkten hinzugefügt
            neuer_weg.besuchte_punkte.add(self.ende)
            k = Kante(self.ende, neues_ende)  # Gewählte Kante
            neuer_weg.kanten.append(k)  # Neue Kante wird zu anderen Kanten
            # hinzugefügt

            # Liste mit Indizes von Abschnitten,
            # die mit den Feldern der neuen Kante zusammenhängen
            haengt_zusammen = []
            for i, a in enumerate(neuer_weg.abschnitte):
                if k.feld1() in a.felder or k.feld2() in a.felder:
                    # Felder der neuen Kante hängen mit Abschnitt a zusammen
                    haengt_zusammen.append(i)

            if len(haengt_zusammen) == 0:

                ''' Kante hängt mit keinem Abschnitt zusammen '''

                # Felder der neuen Kante hängen mit keinem alten Abschnitt
                # zusammen und bilden neuen Abschnitt
                a_neu = Abschnitt(0, [k], {k.feld1(), k.feld2()}, [0])
                x1, y1 = k.feld1()
                x2, y2 = k.feld2()
                diff = matrix[y1][x1] - matrix[y2][x2]  # Differenz der Felder
                if abs(diff) < 1:  # Es muss Erde bewegt werden
                    # Es wird so viele verschoben, dass ein Unterschied von
                    # genau 1 entsteht
                    a_neu.kosten = (1 - abs(diff)) / 2.
                    if diff > 0:
                        a_neu.verschieben = [- (1 - diff) / 2]
                    else:
                        a_neu.verschieben = [(1 + diff) / 2]
                else:  # Es muss keine Erde verschoben werden
                    a_neu.kosten = 0
                neuer_weg.abschnitte.append(a_neu)

            elif len(haengt_zusammen) == 2:

                ''' Kante hängt mit zwei Abschnitten zusammen '''

                # Felder der neuen Kante verbinden zwei Abschnitte,
                # die zu einem Abschnitt gemacht werden
                a1 = neuer_weg.abschnitte[haengt_zusammen[0]]  # 1. Abschnitt
                a2 = neuer_weg.abschnitte[haengt_zusammen[1]]  # 2. Abschnitt
                del neuer_weg.abschnitte[haengt_zusammen[1]]  # 2. Abschnitt wird
                # gelöscht

                # 1. Abschnitt wird erweitert
                a1.kanten.extend(a2.kanten)
                a1.felder |= a2.felder

                del haengt_zusammen[1]

            if len(haengt_zusammen) == 1:

                ''' Abschnitt wird erweitert und neu berechnet '''

                # Kante hängt mit mindestens einem Abschnitt zusammen.
                # Dieser Abschnitt muss erweitert und neu berechnet werden.

                # Abschnitt, der mit der neuen Kante zusammenhängt
                a = neuer_weg.abschnitte[haengt_zusammen[0]]

                # Felder der Kante werden hinzugefügt
                a.felder.add(k.feld1())
                a.felder.add(k.feld2())
                a.kanten.append(k)  # Kante wird hinzugefügt

                bereits_berechnet = False
                # Es wird geprüft, ob der Abschnitt bereits berechnet wurde
                for i in lookup:
                    if i[0] == set(a.kanten):  # Bereits berechnet
                        # Liste mit verschobenen Werten wird geladen
                        a.verschieben = i[1]
                        # Kosten werden berechnet
                        a.kosten = abs_summe(a.verschieben)
                        bereits_berechnet = True
                        break

                if not bereits_berechnet:
                    # Kosten müssen neu berechnet werden
                    a.verschieben = optimum(a.kanten, matrix, 0.00001)

                    # Neue Kosten sind absolute Summe der Verschiebungen
                    a.kosten = abs_summe(a.verschieben)

                    # Kosten und Verschiebungen werden gespeichert,
                    # damit sie nicht noch einmal berechnet werden müssen
                    lookup.append([set(a.kanten), a.verschieben])

            ''' Kosten werden aktualisiert '''

            # Neue Gesamt Kosten werden berechnet.
            # Das ist die Summe der Kosten aller Abschnitte.
            neuer_weg.kosten = sum([a.kosten for a in neuer_weg.abschnitte])

            # Noch mindestens benötigte Kosten werden berechnet
            if k.horizontal():
                # Kante ist horizontal und
                # Kosten ab dem Ende können verwendet werden
                neuer_weg.kosten_ende = neuer_weg.kosten + min_ende[neuer_weg.ende[0]]
            else:
                # Kante ist vertikal und
                # Kosten ab dem Ende können nicht verwendet werden,
                # jedoch müssen mindestens die Kosten
                # ab der Position danach aufgewendet werden
                neuer_weg.kosten_ende = neuer_weg.kosten + min_ende[neuer_weg.ende[0] + 1]
            neuer_weg.kosten_ende = round(neuer_weg.kosten_ende, 4)
            yield neuer_weg  # Weg wird zurückgegeben