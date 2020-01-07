class Enemy:
    def __init__(self):
        raise NotImplementedError("Do not create raw enemy objects!")

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0


class Wolf(Enemy):
    def __init__(self):
        self.name = "Wolf"
        self.hp = 5
        self.damage = 2


class Giant(Enemy):
    def __init__(self):
        self.name = "Giant"
        self.hp = 8
        self.damage = 3


class Minotaur(Enemy):
    def __init__(self):
        self.name = "Minotaur"
        self.hp = 30
        self.damage = 8


class Gryphon(Enemy):
    def __init__(self):
        self.name = "Gryphon"
        self.hp = 20
        self.damage = 6
