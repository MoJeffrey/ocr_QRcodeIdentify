class HSVColor(object):
    lower: tuple = None
    upper: tuple = None
    name: str = None

    def __init__(self, lower: tuple = None, upper: tuple = None, name: str = None):
        self.lower = lower
        self.upper = upper
        self.name = name
