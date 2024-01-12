class KennzeichenFolge:
    """
    Beschreibt eine Kennzeichenfolge.
    Diese setzt sich aus mehreren Kennzeichen zusammen.
    Daneben wird das restliche Wort gespeichert,
    welches noch nicht mit Kennzeichen geschrieben
    wurde und noch zu schreiben ist. Wenn es kein restliches Wort mehr gibt,
    stellt die Kennzeichenfolge ein gesamtes Wort dar.
    """
    def __init__(self, kennzeichen, rest_wort):
        # Liste mit Kennzeichen, die Wort abbilden
        self.kennzeichen_list = kennzeichen.copy()
        # Restliches Wort, das noch nicht auf Kennzeichen verteilt wurde
        self.rest_wort = rest_wort

    def fertig(self):
        # Gesamtes Wort wurde auf Kennzeichen verteilt
        return self.rest_wort == ""
