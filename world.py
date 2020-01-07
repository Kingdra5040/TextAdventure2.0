import random
import enemies
import npc


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return """
        You awaken in a dark and gloomy forest.
        There are four paths you can take.
        Night is quickly approaching, you had better make your way out soon.
        """


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.Wolf()
            self.alive_text = "A wolf is standing in front of you," \
                              " it looks like it hasn't had a good meal in a while! "
            self.dead_text = "The wolf collapses as you strike it down!"
        elif r < 0.80:
            self.enemy = enemies.Giant()
            self.alive_text = "A Giant guards the path ahead, \n he looks tall and angry!"
            self.dead_text = "The ground around you shakes as the Giant falls!"
        elif r < 0.91:
            self.enemy = enemies.Gryphon()
            self.alive_text = "A Gryphon swoops down from the sky and attacks you!"
            self.dead_text = "The Gryphon screeches and falls over, dead!"
        else:
            self.enemy = enemies.Minotaur()
            self.alive_text = "A fearsome Minotaur stomps his foot down ready for battle."
            self.dead_text = "You have slain the Minotaur!"

        super().__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("You got hit and took {} damage! You have {} HP remaining.".format(self.enemy.damage, player.hp))


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Gold".format(i, item.name, item.value))
        while True:
            user_input = input("Choose an item or press Q to leave: ")
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Invalid choice")

    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("Sorry, the item you have chosen is too expensive.")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print("Thanks for trading!  Hope to see you again!")

    def check_if_trade(self, player):
        while True:
            print("Would you like to buy(B), sell(S), or quit(Q) ?")
            user_input = input()
            if user_input in ['q', 'Q']:
                return
            elif user_input in ['b', 'b']:
                print("What would you like?: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                print("Here is what is available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid action.")

    def intro_text(self):
        return """
        You have come across a strange hooded man.
        He calls out to you asking if you would like to trade.
        """


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(5, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print("+{} gold.".format(self.gold))

    def intro_text(self):
        if self.gold_claimed:
            return"""
            Its getting dark, you should hurry!
            """
        else:
            return"""
            You found a small bag of gold. \n Finders, keepers!
            """


class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True

    def intro_text(self):
        return """
        You feel the warmth of the sun cover you. 
        You have escaped to safety.
        
        VICTORY!
        """


world_dsl = """
|FG|FG|EN|TT|VT|
|FG|EN|FG|EN|EN|
|EN|ST|EN|  |FG|
|  |EN|EN|EN|EN|
|FG|FG|TT|FG|EN|

"""


def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True


tile_type_dict = {"VT": VictoryTile, "EN": EnemyTile, "ST": StartTile, "TT": TraderTile, "FG": FindGoldTile, "  ": None}


world_map = []

start_tile_location = None


def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
                row.append(tile_type(x, y) if tile_type else None)

            world_map.append(row)


def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None
