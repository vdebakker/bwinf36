from scipy.optimize import minimize
from numpy import array, zeros


def optimum(kanten, matrix, toleranz):
    """ Optimale Verschiebung von Erde wird berechnet
    :param kanten: Kanten, an denen ein Höhenunterschied von mind. 1m
    entstehen  soll
    :param matrix: Matrix mit Höhen der Planquadrate
    :param toleranz: Genauigkeit der Ungleichungen
    :return: Liste mit Werten, wieviel an jeder Kante verschoben wird
    """

    anfangs_differenzen = []  # Liste mit Differenzen an den Kanten zu Beginn
    for k in kanten:
        x1, y1 = k.feld1()
        x2, y2 = k.feld2()
        diff = matrix[y1][x1] - matrix[y2][x2]
        anfangs_differenzen.append(diff)

    # Liste mit den beiden Feldern jeder Kante, zwischen denen die Kante liegt
    felder = []
    for k in kanten:
        felder.append((k.feld1(), k.feld2()))

    ''' Einfluss Matrix erstellen '''

    #   Matrix, die besagt, wieviel jede Verschiebung die Differenz jeder Kante
    #   beeinflusst
    einfluss = []
    for i, differenz_felder in enumerate(felder):
        einfluss.append([])
        # Felder, deren Differenz beeinflusst wird
        feld1, feld2 = differenz_felder
        for j, verschieben in enumerate(felder):
            if i == j:
                # Die Felder, zwischen denen die Differenz gemessen wird,
                # sind die gleichen, zwischen denen die Erde verschoben wird.
                einfluss[i].append(-2)
            elif feld1 == verschieben[1]:  # Erde wird zu Feld1 verschoben
                einfluss[i].append(1)
            elif feld1 == verschieben[0]:  # Erde wird von Feld1 verschoben
                einfluss[i].append(-1)
            elif feld2 == verschieben[1]:  # Erde wird zu Feld2 verschoben
                einfluss[i].append(-1)
            elif feld2 == verschieben[0]:  # Erde wird von Feld2 verschoben
                einfluss[i].append(1)
            else:  # Differenz wird nicht duch Verschieben beeinflusst
                einfluss[i].append(0)
        einfluss[i] = array(einfluss[i])  # Zeile wird zum Array gemacht


    ''' Bedingungen erstellen '''

    bedingungen = []  # Liste mit Bedingungen
    for i in range(len(kanten)):
        # Jeder Höhenunterschied wird als Ungleichung hinzugefügt
        bedingungen.append({'type': 'ineq', 'fun': fun(einfluss[i],
                                                       anfangs_differenzen[i])})

    ''' Startwerte optimieren '''

    # Liste mit Werten, wieviel an jeder Kante verschoben wird
    verschieben = zeros(len(kanten))
    # Liste wird optimiert
    for i in range(len(kanten)):
        # Summe für -0.5, 0 und 0.5 wird berechnet
        verschieben[i] = - .5
        s1 = sum([b['fun'](verschieben) for b in bedingungen if
                  b['fun'](verschieben) < 0])
        verschieben[i] = .5
        s2 = sum([b['fun'](verschieben) for b in bedingungen if
                  b['fun'](verschieben) < 0])
        verschieben[i] = 0
        s3 = sum([b['fun'](verschieben) for b in bedingungen if
                  b['fun'](verschieben) < 0])
        # Beste Version wird behalten
        if s1 > s3 and s1 > s2:
            verschieben[i] = - .5
        elif s2 > s3 and s2 > s1:
            verschieben[i] = .5
        else:
            verschieben[i] = 0

    ''' Optimum finden '''

    # Optimum wird gesucht, indem minimize aufgerufen wird.
    # Die Funktion, die minimiert werden soll, ist die absolute Summe 'summe'
    ergebnis = minimize(abs_summe, verschieben,
                        constraints=bedingungen, tol=toleranz)
    return ergebnis.x


def fun(einfluss, anfangswert):
    # Hilfsfunktion, um Ungleichung zu erstellen
    return lambda x: abs(sum(x * einfluss) + anfangswert) - 1


def abs_summe(x):
    # Summe der Absoluten Zahlen
    return sum([abs(i) for i in x])
