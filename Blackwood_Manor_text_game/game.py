# Kevin Rogers
import random # for dice!
import time # For slow text!
# import pygame # For music!
import re # I'm not sure what this is for. Comparing things?
import os # Used for clearing the terminal. like this: os.system('cls')

# charactor creator. 
class DnDCharacter:
    point_buy_cost = {
        8: 0, 9: 1, 10: 2, 11: 3, 12: 4,
        13: 5, 14: 7, 15: 9
    }
    
    def ability_scores(self):
        ''' the porpus of this, is to keep track of the player's ability scores.'''
        self.abil = {
            "Strength": 8,
            "Dexterity": 8,
            "Constitution": 8,
            "Intelligence": 8,
            "Wisdom": 8,
            "Charisma": 8
        }
        self.max_points = 27

    def calcu_cost(self):
        return sum(self.point_buy_cost[score] for score in self.abil.values())

    def allocate_ability_scores(self):
        spent_points = self.calcu_cost()
        while True:
            print("\nCurrent Ability Scores:")
            for ability, score in self.abil.items():
                print(f"{ability}: {score}")
            print(f"Points Remaining: {self.max_points - spent_points}")

            choice = input("Which ability would you like to change? (or type 'done' to finish): ").title()
            if choice == "Done":
                break
            if choice not in self.abil:
                print("Invalid ability name.")
                continue

            try:
                new_score = int(input(f"Enter new score for {choice} (8-15): "))
                if new_score < 8 or new_score > 15:
                    print("Ability score must be between 8 and 15.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue

            temp = self.abil.copy()
            temp[choice] = new_score
            new_cost = sum(self.point_buy_cost[score] for score in temp.values())

            if new_cost > self.max_points:
                print("Not enough points for that change.")
            else:
                self.abil[choice] = new_score
                spent_points = new_cost

    def apply_bonus(self):
        print("\nChoose your ability score bonus method:")
        print("1. +2 to one ability, +1 to another")
        print("2. +1 to three different abil")

        choice = input("Enter 1 or 2: ")
        used = []

        if choice == "1":
            for i in range(2):
                while True:
                    ability = input(f"Enter ability for {'+2' if i == 0 else '+1'} bonus: ").title()
                    if ability not in self.abil or ability in used:
                        print("Invalid or duplicate ability.")
                        continue
                    self.abil[ability] += 2 if i == 0 else 1
                    used.append(ability)
                    break
        elif choice == "2":
            for i in range(3):
                while True:
                    ability = input(f"Enter ability #{i+1} for +1 bonus: ").title()
                    if ability not in self.abil or ability in used:
                        print("Invalid or duplicate ability.")
                        continue
                    self.abil[ability] += 1
                    used.append(ability)
                    break
        else:
            print("Invalid choice. No bonuses applied.")
        ''' commented this out. mm
    def mod(self):
        return {
            "Str": (user.abil["Strength"] - 10) // 2,
            "Dex": (user.abil["Dexterity"] - 10) // 2,
            "Con": (user.abil["Constitution"] - 10) // 2,
            "Int": (user.abil["Intelligence"] - 10) // 2,
            "Wis": (user.abil["Wisdom"] - 10) // 2,
            "Cha": (user.abil["Charisma"] - 10) // 2
        }
        '''
    # Final 🎲
    def display_summary(self):
        modifiers = self.mod()
        print("\n Character Stats:")
        print("-------------------------")
        for short, full in zip(["Str", "Dex", "Con", "Int", "Wis", "Cha"], self.abil):
            mod = modifiers[short]
            sign = "+" if mod >= 0 else ""
            print(f"{short} ({self.abil[full]}): {sign}{mod}")
        print("-------------------------")
user = DnDCharacter()

''' stats. commands: user.
To pull the full stat
user.abil("Strength")

'''
class player:
    def __init__(self, abil):
        self.str_ = (abil["Strength"] - 10) // 2
        self.dex_ = (abil["Dexterity"] - 10) // 2
        self.con_ = (abil["Constitution"] - 10) // 2
        self.int_ = (abil["Intelligence"] - 10) // 2
        self.wis_ = (abil["Wisdom"] - 10) // 2
        self.cha_ = (abil["Charisma"] - 10) // 2

        self.hp = 12 + self.con_  # Base HP 
        self.ac = 10 + self.dex_  # Unarmored AC
        #Invintory. These arnt used yet.
        self.red_key = False
        self.bucket = False
        self.sword = False
        self.Food = 1
# player = player(user.abil)

''' example commands. 
player.str_
'''


class DiceRoller:
    dice_pattern = re.compile(r"(\d+)d(\d+)")
    
    @staticmethod
    def dice(expression: str, mod: int = 0) -> int:
        #Rolls dice based on the 'NdM' format (e.g. '2d6') with an optional modifier and prints out things.
        match = DiceRoller.dice_pattern.fullmatch(expression.lower().strip())
        if not match:
            raise ValueError(f"Invalid dice expression: {expression}")
        
        num, sides = map(int, match.groups())
        rolls = [random.randint(1, sides) for _ in range(num)]
        total = sum(rolls) + mod
        if mod:
            print(f"🎲 {expression}: {rolls} + {mod} → {total}")
        else:
            print(f"🎲 {expression}: {rolls} → {total}")
        return total
    
    @staticmethod
    def dice_num(expression: str, mod: int = 0) -> int:
        #Rolls dice and only returns the number
        match = DiceRoller.dice_pattern.fullmatch(expression.lower().strip())
        if not match:
            raise ValueError(f"Invalid dice expression: {expression}")
        
        num, sides = map(int, match.groups())
        rolls = [random.randint(1, sides) for _ in range(num)]
        total = sum(rolls) + mod
        return total

    @staticmethod
    def adv(mod: int = 0) -> int:
        """Rolls 1d20 with advantage (keep highest), with optional modifier."""
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        result = max(roll1, roll2)
        total = result + mod

        if mod != 0:
            print(f"🎲 Advantage(d20): {roll1}, {roll2} {result} + {mod} → {total}")
        else:
            print(f"🎲 Advantage(d20): {roll1}, {roll2} → {result}")

        return total

    @staticmethod
    def dis(mod: int = 0) -> int:
        """Rolls 1d20 with disadvantage (keep lowest), with optional modifier."""
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        result = min(roll1, roll2)
        total = result + mod

        if mod != 0:
            print(f"🎲 Disadvantage(d20): {roll1}, {roll2}: {result} + {mod} → {total}")
        else:
            print(f"🎲 Disadvantage(d20): {roll1}, {roll2} → {result}")

        return total
roll = DiceRoller()
''' Diceroller commands:
if roll.dice("2d6") >= 10:
roll.dice("3d4", mod = 5) 
if roll.adv(mod = player.dex_) >= 15:
if roll.dis() >= 16:
roll.dice_num("1d4") + 3
'''

class Monstermaker:
    def __init__(self, name, hp, dex, melee_damage, str_, range_):
        self.name = name
        self.hp = hp
        self.ac = 10 + dex
        self.dex = dex
        self.str = str_
        self.melee_formula = melee_damage
        self.range = range_

    def melee_damage(self):
        return roll.dice_num(self.melee_formula) + self.str
    
    ''' not useing this because lack of time.
    def range_damage(self):
        return roll.dice_num(self.melee_formula) + self.dex'''

# Factory function!
def monster_factory(name):
    MONSTER_DATA = {
        "book mimic": {"hp": 7, "dex": 1, "melee_damage": "1d4", "str_": 1, "range_": 5},
        "skeleton": {"hp": 10, "dex": 2, "melee_damage": "1d4", "str_": 1, "range_": 25},
        # Add more monsters here!
    }

    # If the monster name exists, return a new Monster instance
    if name in MONSTER_DATA:
        data = MONSTER_DATA[name]
        return Monstermaker(name, **data)

    # If the monster name doesn't exist, raise an error
    raise ValueError(f"Monster '{name}' not found.")
book_mimic = monster_factory("book mimic")
''' Commands from this class that can be used.
book_mimic.melee_damage()
goblin_chief = Monstermaker("goblin chief", hp=30, dex=3, melee_damage="2d4", str_=2, range_=15) #I think this one could be used in a terminal
'''
class Combat:
    def __init__(self, player, monster_names: list[str]):
        self.player = player
        self.monsters = [monster_factory(name) for name in monster_names]
        self.combatants = []

    def roll_initiative(self, mod):
        return roll.dice_num("1d20") + mod

    def start(self):
        print("\n🛡️ COMBAT STARTS!\n")

        # Roll initiative for player
        self.combatants.append((self.roll_initiative(self.player.dex_), "player"))

        # Roll initiative for each monster
        for m in self.monsters:
            self.combatants.append((self.roll_initiative(m.dex), m))

        # Sort by initiative (descending)
        self.combatants.sort(reverse=True, key=lambda x: x[0])

        print("🌀 Initiative Order:")
        for init, entity in self.combatants:
            name = entity.name if isinstance(entity, Monstermaker) else "Player"
            print(f"{name}: {init}")
        print()

        # Main combat loop
        while self.player.hp > 0 and any(m.hp > 0 for m in self.monsters):
            for _, entity in self.combatants:
                if isinstance(entity, str) and entity == "player":
                    self.player_turn()
                elif isinstance(entity, Monstermaker) and entity.hp > 0:
                    self.monster_turn(entity)

                # Check end conditions early
                if self.player.hp <= 0:
                    break
                if all(m.hp <= 0 for m in self.monsters):
                    break

        # Final results
        if self.player.hp <= 0:
            print("\n💀 You have been defeated...")
        else:
            print("\n🏆 You are victorious!")

    def player_turn(self):
        print("\n🧍 Your turn!")
        target = self.choose_target()
        if not target:
            return

        hit_roll = roll.dice_num("1d20") + self.player.str_
        print(f"You swing your weapon at {target.name} (AC {target.ac}) → To Hit: {hit_roll}")
        if hit_roll >= target.ac:
            dmg = roll.dice_num("1d8") + self.player.str_
            target.hp -= dmg
            print(f"💥 You hit {target.name} for {dmg} damage! (HP left: {target.hp})")
            if target.hp <= 0:
                print(f"☠️ {target.name} is defeated!")
        else:
            print(f"💨 You missed {target.name}.")

    def choose_target(self):
        alive = [m for m in self.monsters if m.hp > 0]
        if not alive:
            return None

        if len(alive) == 1:
            return alive[0]

        print("Choose a target:")
        for i, m in enumerate(alive, 1):
            print(f"{i}: {m.name} (HP: {m.hp})")
        while True:
            try:
                choice = int(input("Target #: "))
                if 1 <= choice <= len(alive):
                    return alive[choice - 1]
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Enter a number.")

    def monster_turn(self, monster):
        print(f"\n👹 {monster.name}'s turn:")
        hit_roll = roll.dice_num("1d20") + monster.str
        print(f"{monster.name} attacks you (AC {self.player.ac}) → To Hit: {hit_roll}")
        if hit_roll >= self.player.ac:
            dmg = monster.melee_damage()
            self.player.hp -= dmg
            print(f"💥 {monster.name} hits you for {dmg} damage! (Your HP goes to: {self.player.hp})")
        else:
            print(f"{monster.name} missed!")

skip = False  # Set this to True to skip character creation and use default stats

def start_character_creation():
    global user
    global player
    user = DnDCharacter()

    if skip:
        # Skip character creation and set all stats to 14 for dev testing
        user.abil = {
            "Strength": 14,
            "Dexterity": 14,
            "Constitution": 14,
            "Intelligence": 14,
            "Wisdom": 14,
            "Charisma": 14
        }
        print("⚙️ Dev mode is active: All stats are set to 14.")
    else:
        user.ability_scores()
        user.allocate_ability_scores()
        user.apply_bonus()

    player = player(user.abil)
    print("\n🪞 As you finish adjusting your coat, your reflection seems... sharper. More *real*.")
    print("🧍 You are ready.")
    return player

''' I need to work on the volume mixer. 
def play_sound(file_path, volume=0.4): 
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)
'''

def play_music(file_path, volume=0.4):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1) #looping until stopped.

'''
pygame.mixer.music.fadeout(2000) 
'''

# makin a slow print for drimatic effect!
def slow_print(text, delay=0.05): 
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def slow_print_lines(text, delay = 1):  # delay in seconds between lines
    for line in text.splitlines():
        print(line)
        time.sleep(delay)

def intro_teacher():
    os.system('cls')
    print("")
    print("Hello professor!, this is my project!")
    print("I've worked About 15+ hours on it and I plan to work on it even more in the future!")
    print("This program uses audio so headphones are recomended.")
    print("But without further adue, this is what I have so far:")
    input("Press enter to continue:")
    os.system('cls')


def intro_scene():
    play_music("music/Nostalgia.mp3")
    os.system('cls')
    print("")
    slow_print("Welcome to the Mystery at Blackwood Manor!", 0.02)
    print("")
    time.sleep(1)
    slow_print("It begins on a rainy evening...", 0.15)
    time.sleep(1.55)
    slow_print("You've been enjoying a home cooked meal when you hear a knock on your door.", 0.06)
    # play_sound("music\door-knocking-1.mp3") # I can't get this sound right. 
    time.sleep(1.5)
    slow_print("You open the door to see a single a letter on the foot of your door. It's sealed in wax, bearing a raven crest...", 0.04)
    slow_print("The letter says that you are the last known heir of Reginald Blackwood.", 0.04)
    slow_print("A man whose name the locals still whisper with unease.", 0.04)
    time.sleep(1)
    slow_print("\nIn his will, one condition was clear:")
    slow_print("Survive five nights in Blackwood Manor, and all I possess shall be yours.")
    slow_print("\"if you fail, the mansion and all that remains will be destroyed\"\n")
    time.sleep(1.5)
    slow_print("Fog coils around the wrought iron gate as the carriage pulls away, leaving you alone in the rain.")
    slow_print("The Manor looms before you — shuttered windows, crooked chimneys, and a door that groans as it opens by itself...\n")
    time.sleep(2)
    slow_print("You step into the dim foyer. Dust coats the air. The smell of age and secrets hangs heavy.\n")
    slow_print("A grand mirror on the wall catches your reflection. You pause.\n")
    time.sleep(2)
    slow_print("You look into your own eyes...\n")
    time.sleep(3)
    os.system('cls')
    # Launched character creation
    start_character_creation()

def library_intro():
    slow_print("\n👞 You hear footsteps echoing through the hall.", 0.04)
    slow_print("From the shadows, an old man in a sharp but dusty suit emerges — the manor's butler.", 0.04)
    slow_print("\n\"Ah! You must be the heir. Welcome to Blackwood Manor,\" he says with a raspy smile.", 0.04)

    time.sleep(1)
    slow_print("\"Allow me to take your coat and belongings,\" he offers, with a slight bow.")
    slow_print("Before you can answer, he deftly relieves you of your pack and coat with surprising strength.")

    time.sleep(1.5)
    slow_print("\n\"Please, make yourself comfortable in the library,\" he continues.")
    slow_print("\"I shall return shortly with a spot of tea. Don't wander.\"\n")

    slow_print("With a nod, he turns and disappears deeper into the manor.", 0.04)
    slow_print("You are left alone in the flickering firelight of the manor's grand library.", 0.04)

    time.sleep(1.5)
    slow_print("Books line every wall. Dust dances in the air. You hear... something shift in the book cases.\n", 0.04)


def start_combat_mimic():
    pygame.mixer.music.fadeout(2000)
    time.sleep(2)
    play_music("music/Aberration Fight shortend.mp3")
    combat = Combat(player, ["book mimic"])
    combat.start()
    
art_title = """
 ▄▄▄▄    ██▓    ▄▄▄       ▄████▄   ██ ▄█▀ █     █░ ▒█████   ▒█████  ▓█████▄     ███▄ ▄███▓ ▄▄▄       ███▄    █  ▒█████   ██▀███  
▓█████▄ ▓██▒   ▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█░ █ ░█░▒██▒  ██▒▒██▒  ██▒▒██▀ ██▌   ▓██▒▀█▀ ██▒▒████▄     ██ ▀█   █ ▒██▒  ██▒▓██ ▒ ██▒
▒██▒ ▄██▒██░   ▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒█░ █ ░█ ▒██░  ██▒▒██░  ██▒░██   █▌   ▓██    ▓██░▒██  ▀█▄  ▓██  ▀█ ██▒▒██░  ██▒▓██ ░▄█ ▒
▒██░█▀  ▒██░   ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ░█░ █ ░█ ▒██   ██░▒██   ██░░▓█▄   ▌   ▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒▒██   ██░▒██▀▀█▄  
░▓█  ▀█▓░██████▒▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░░██▒██▓ ░ ████▓▒░░ ████▓▒░░▒████▓    ▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░░ ████▓▒░░██▓ ▒██▒
░▒▓███▀▒░ ▒░▓  ░▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒░▒░▒░  ▒▒▓  ▒    ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
▒░▒   ░ ░ ░ ▒  ░ ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░  ▒ ░ ░    ░ ▒ ▒░   ░ ▒ ▒░  ░ ▒  ▒    ░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░   ░▒ ░ ▒░
 ░    ░   ░ ░    ░   ▒   ░        ░ ░░ ░   ░   ░  ░ ░ ░ ▒  ░ ░ ░ ▒   ░ ░  ░    ░      ░     ░   ▒      ░   ░ ░ ░ ░ ░ ▒    ░░   ░ 
 ░          ░  ░     ░  ░░ ░      ░  ░       ░        ░ ░      ░ ░     ░              ░         ░  ░         ░     ░ ░     ░     
      ░                  ░                                           ░                                                           
"""
art_keys = """
                         
        _______           
       |\     /|          
       | +---+ |          
       | |   | |          
       | |W  | |          
       | +---+ |          
       |/_____\|                                   
 _______ _______ _______ 
|\     /|\     /|\     /|
| +---+ | +---+ | +---+ |
| |   | | |   | | |   | |
| |A  | | |S  | | |D  | |
| +---+ | +---+ | +---+ |
|/_____\|/_____\|/_____\|
                         
"""

# Start the game

intro_teacher()
slow_print("Welcome to...", 0.2)
print("")
print("")
slow_print_lines(art_title)
input("")

intro_scene()

library_intro()
start_combat_mimic()
