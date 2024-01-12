class Person:
    """
    Simuliert eine Person. Diese besitzt einen Namen und
    Personen mit denen sie das Zimmer teilen bzw. nicht teilen möchte
    """
    def __init__(self, name: str, teilen: iter, nicht_teilen: iter):
        self.name = name  # String mit Namen der Person
        # Listen mit Namen, mit denen diese Person
        # ein Zimmer teilen bzw. nicht teilen möchte
        self.teilen = teilen
        self.nicht_teilen = nicht_teilen

    def __repr__(self):
        # Person wird mit dem Namen beim Ausgeben dargestellt
        return self.name
