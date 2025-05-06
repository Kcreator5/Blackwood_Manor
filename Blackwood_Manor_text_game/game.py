# Kevin Rogers
import random # for dice!
import time # For slow text!
import pygame # For music!
import re # This is for comparing things.
import os # Used for clearing the terminal. like this: os.system('cls')

# charactor creator. 
class DnDCharacter:
    point_buy_cost = {
        8: 0, 9: 1, 10: 2, 11: 3, 12: 4,
        13: 5, 14: 7, 15: 9
    }

    def ability_scores(self):
        '''this creates the ability scores'''
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
        '''this cacluates the point buy cost system.'''
        return sum(self.point_buy_cost[score] for score in self.abil.values())

    def allocate_ability_scores(self):
        '''This updates the ability scores'''
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
        '''this adds a few more bonus to the ability scores.'''
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
        '''This function defines the modifires for the player's abilities as well as sets Hit Points & Armor Class'''
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
        '''Rolls dice based on the 'NdN' format (e.g. '2d6') with an optional modifier and prints out things.'''
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
        '''Rolls dice and only returns the number'''
        match = DiceRoller.dice_pattern.fullmatch(expression.lower().strip())
        if not match:
            raise ValueError(f"Invalid dice expression: {expression}")
        
        num, sides = map(int, match.groups())
        rolls = [random.randint(1, sides) for _ in range(num)]
        total = sum(rolls) + mod
        return total

    @staticmethod
    def adv(mod: int = 0) -> int:
        '''Rolls 1d20 with advantage (keep highest), with optional modifier.'''
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
        '''Rolls 1d20 with disadvantage (keep lowest), with optional modifier.'''
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
        '''This works with the later functions, makes veribles for monsters'''
        self.name = name
        self.hp = hp
        self.ac = 10 + dex
        self.dex = dex
        self.str = str_
        self.melee_formula = melee_damage
        self.range = range_

    def melee_damage(self):
        '''this is the melle damage the monster dose'''
        return roll.dice_num(self.melee_formula) + self.str
    
    ''' not useing this because lack of time.
    def range_damage(self):
    This is for a feuture ranged attack
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
        '''This works with the later functions as well as the monsterfactory'''
        self.player = player
        self.monsters = [monster_factory(name) for name in monster_names]
        self.combatants = []

    def roll_initiative(self, mod):
        '''This decides who goes first and in what order of combat'''
        return roll.dice_num("1d20") + mod

    def start(self):
        '''This starts combat'''
        os.system('cls')
        slow_print("\n🛡️  ROLL INITIATIVE!", 0.03)
        time.sleep(1)

        # Initiative rolls
        p_init = self.roll_initiative(self.player.dex_)
        self.combatants.append((p_init, "player"))
        slow_print(f"🎲 You rolled: {p_init}", 0.03)

        for m in self.monsters:
            m_init = self.roll_initiative(m.dex)
            self.combatants.append((m_init, m))
            slow_print(f"👹 {m.name} rolled: {m_init} on initiative", 0.03)
            time.sleep(1)

        self.combatants.sort(reverse=True, key=lambda x: x[0])

        slow_print("\n🌀 Initiative Order:", 0.02)
        for init, entity in self.combatants:
            name = entity.name if isinstance(entity, Monstermaker) else "Player"
            slow_print(f"• {name}: {init}", 0.02)
        print()
        time.sleep(1.5)

        # Combat loop
        while self.player.hp > 0 and any(m.hp > 0 for m in self.monsters):
            for _, entity in self.combatants:
                if isinstance(entity, str) and entity == "player":
                    self.player_turn()
                elif isinstance(entity, Monstermaker) and entity.hp > 0:
                    self.monster_turn(entity)

                if self.player.hp <= 0 or all(m.hp <= 0 for m in self.monsters):
                    break

        if self.player.hp <= 0:
            pygame.mixer.music.fadeout(2050)
            slow_print("\n💀 You have been defeated...", 0.06)
            play_sound("music/gta-v-death.mp3")
            time.sleep(4)
            slow_print("Thanks for playing! Thats all I have so far...")
            time.sleep(4)
        else:
            pygame.mixer.music.fadeout(2050)
            slow_print("The monster falls, defeted")
            slow_print("\n🏆 You are victorious!", 0.02)
            play_sound("music/final-fantasy-vii-victory.mp3")
            time.sleep(4)
            slow_print("Thanks for playing! Thats all I have so far...")
            time.sleep(4)

    def player_turn(self):
        '''This dose the turn for the player!'''
        slow_print("\n🧍 Your Turn", 0.03)
        print(f"💖 HP: {self.player.hp}   🛡️ AC: {self.player.ac}")
        print(f"🎯 Actions:")
        print(f"1: Attack (+{self.player.str_} to hit, 1d8+{self.player.str_} damage)")

        while True:
            action = input("Choose an action: ").strip()
            if action == "1":
                target = self.choose_target()
                if not target:
                    return
                hit_roll = roll.dice_num("1d20") + self.player.str_
                slow_print(f"\nYou swing at {target.name} (AC {target.ac}) → To Hit: {hit_roll}", 0.02)
                if hit_roll >= target.ac:
                    dmg = roll.dice_num("1d8") + self.player.str_
                    target.hp -= dmg
                    slow_print(f"💥 Hit! You dealt {dmg} damage. (HP left: {target.hp})", 0.02)
                    if target.hp <= 0:
                        slow_print(f"☠️ {target.name} is defeated!", 0.02)
                else:
                    slow_print("💨 You missed!", 0.02)
                time.sleep(2)
                os.system('cls')
                break
            else:
                print("Invalid choice. Try again.")

    def monster_turn(self, monster):
        '''this dose the turn for the monster'''
        slow_print(f"\n👹 {monster.name}'s Turn", 0.03)
        hit_roll = roll.dice_num("1d20") + monster.str
        slow_print(f"{monster.name} attacks! (To Hit: {hit_roll} vs AC {self.player.ac})", 0.02)
        if hit_roll >= self.player.ac:
            dmg = monster.melee_damage()
            self.player.hp -= dmg
            slow_print(f"💥 {monster.name} hits you for {dmg} damage! (Your HP: {self.player.hp})", 0.02)
        else:
            slow_print(f"{monster.name} misses!", 0.02)
        time.sleep(1.5)

    def choose_target(self):
        '''checks to see if the monster or player is at 0'''
        alive = [m for m in self.monsters if m.hp > 0]
        if not alive:
            return None
        if len(alive) == 1:
            return alive[0]
        print("\nChoose a target:")
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


# Setup function(s)
def setup_music():
    '''This helps other fuctions not have error problems when a song changes'''
    # 🎵 Ensure mixer is initialized
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # 🔇 Fade out current music if any
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(3000)
        time.sleep(3)

def setup_player(player_obj=None): 
    ''' 🧍 Create default player if none is passed'''
    if player_obj is None:
        default_stats = {
            "Strength": 14,
            "Dexterity": 14,
            "Constitution": 14,
            "Intelligence": 14,
            "Wisdom": 14,
            "Charisma": 14
        }
        player_obj = player(default_stats)
        print ("🧪 No player passed. Created default test player.")
    return player_obj


skip = False  # Set this to True to skip character creation and use default stats

def start_character_creation():
    '''This starts the character creation, however it's a tad time consuming. This also was one of the most problematic things to get right.'''
    slow_print("Choose your stats! *Note: there is only one combat encounter. Str, Dex, and Con are only used so far.")
    time.sleep(2)

    global user  # Keep this if you need `user` to be accessible globally
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

    # 💡 Rename the variable so we don't overwrite the class `player`
    player_instance = player(user.abil)
    
    slow_print("\n🪞 As you finish adjusting your coat, your reflection seems... sharper. More *real*.")
    slow_print("🧍 You are ready.")
    time.sleep(2)

    return player_instance

def play_music(file_path, volume=0.4):
    '''This takes a song from the music folder plays it, it does go on loop'''
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1) #looping until stopped.
'''
pygame.mixer.music.fadeout(2000) 
'''
def play_sound(file_path, volume=0.4):
    '''This takes a sound from the music folder plays it, it dosn't go on loop'''
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    try:
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(volume)
        sound.play()
    except pygame.error:
        print(f"⚠️ Could not play sound: {file_path}")

# 
def slow_print(text, delay=0.05): 
    '''makin a slow print for drimatic effect!'''
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def intro_teacher():
    '''This says hello to my professor! It aslo explains some things to the user'''
    os.system('cls')
    print("")
    print("Hello professor!, this is my project!")
    print("I've worked About 15+ hours on it and I plan to work on it even more in the future!")
    print("This program uses audio so headphones are recomended.")
    print("But without further adue, this is what I have so far:")
    input("Press enter to continue:")

def intro_scene():
    '''This introduces the story and playes music to set the scene'''
    play_music("music/Nostalgia.mp3")
    os.system('cls')
    print("")
    slow_print("Welcome to the Mystery at Blackwood Manor!", 0.02)
    print("")
    time.sleep(1)
    slow_print("It begins on a rainy evening...", 0.15)
    time.sleep(1.55)
    slow_print("You've been enjoying a home cooked meal when you hear a knock on your door.", 0.06)
    play_sound("music\door-knocking-1.mp3", volume = 0.4) # I got this working!
    time.sleep(1.5)
    slow_print("You open the door so see a single letter on the foot of your door. It's sealed in wax, bearing a raven crest...", 0.04)
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

def library_intro():
    '''This continues the story'''
    os.system('cls')
    slow_print(f"\n👞 You hear {roll.dice_num("1d4") + 1 } footsteps echoing through the hall.", 0.04)
    slow_print("From the shadows, an old man in a sharp but dusty suit emerges — the manor's butler.", 0.06)
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
    slow_print("and then you see it, a book fly out towards you, but it has teeth!?")
    input("press enter")
    os.system('cls')

def start_combat_mimic(player_obj=None):
    '''This sets up combat, like music and stats.'''
    setup_music()
    # 🧍 Ensure player exists
    player_obj = setup_player(player_obj)

    # 🎵 Load combat music safely
    try:
        play_music("music/Aberration Fight shortend.mp3")
    except pygame.error:
        print("⚠️ Could not load combat music. Continuing without it.")

    # ⚔️ Start combat
    combat = Combat(player_obj, ["book mimic"])
    combat.start()

# Start the game '''

intro_teacher()

intro_scene()

created_player = start_character_creation() 
'''This was a fix I found that helped with a problem I was having.'''

library_intro()

start_combat_mimic()
# end of the game so far.