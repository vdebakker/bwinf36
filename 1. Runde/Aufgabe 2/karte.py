class Karte:
    """
    Stellt eine Karte dar.
    Dabei werden ihr Name und die Anzahl an Jugendlichen und Erwachsenen,
    die mit dieser Karte in das Schwimmbad können, gespeichert
    """
    def __init__(self, name, jugendliche, erwachsene):
        self.name = name  # Name der Karte
        # Anzahl an Jugendlichen,
        # die mit der Karte in das Schwimmbad gehen können
        self.jugendliche = jugendliche
        # Anzahl an Erwachsenen,
        # die mit der Karte in das Schwimmbad gehen können
        self.erwachsene = erwachsene
