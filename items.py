class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)


class Bread(Consumable):
    def __init__(self):
        self.name = "Bread"
        self.healing_value = 10
        self.value = 10


class PotionOfHealth(Consumable):
    def __init__(self):
        self.name = "Potion of Health"
        self.healing_value = 25
        self.value = 25

# Weapons


class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects.")

    def __str__(self):
        return self.name


class Knife(Weapon):
    def __init__(self):
        self.name = "Knife"
        self.description = "A small sharp blade."
        self.damage = 3
        self.value = 1

class ShortSword(Weapon):
    def __init__(self):
        self.name = "Short Sword"
        self.description = "A sturdy sword."
        self.damage = 6
        self.value = 20


class GreatSword(Weapon):
    def __init__(self):
        self.name = "Great Sword"
        self.description = "A mighty sword that only few have had the honor to wield."
        self.damage = 15
        self.value = 60


class ShortBow(Weapon):
    def __init__(self):
        self.name = "Short Bow"
        self.description = "A bow crafted from an oak tree."
        self.damage = 5
        self.value = 18


class Crossbow(Weapon):
    def __init__(self):
        self.name = "Crossbow"
        self.description = "A modern adaptation, used by fearsome archers."
        self.damage = 12
        self.value = 50

