"""
game.py

part of the Text Based RPG project.
this is a wapper for the other 'text based rpg' modules.

By: Calacuda | MIT Licence | Epoch: ? | version date: October 22th, 2019
"""


import numpy as np
import equipment as eq
import items as itm
import people as ppl
import enemies as enm
import world


class Game:
    def __init__(self, world_name, world_size=(2, 2), auto_agro=True):
        """
        self.world refers to an instance off the world object.
        self.characters is a dictionary that holds the name of a character 
        as a key and their value is a tuple of their location and then
        the object its self. 
        self.items is a dictionary where the key is the name of an item 
        and the value is a set of tuples. the tuples each represent a 
        specific instance of that item, their first indecie is location 
        of the item and the second is the item object its self.  
        self. zones is a dictionary that holds the indexes of the zone as its 
        keys and the zone object its self as its value. 
        """
        self.zones = np.array([[None]*world_size[1]]*world_size[0])
        for row in range(world_size[0]):
            for col in range(world_size[1]):
                self.zones[row, col] = world.Zone(f"{row} {col}", "auto generated zone")
                c_zone = (row, col)
                if col != 0:
                    l_zone = (row, col-1)
                    self.alter_road(c_zone, l_zone) #, 'w')
                if row != 0:
                    l_zone = (row-1, col)
                    self.alter_road(c_zone, l_zone) #, 'n')
        self.world = None
        self.player = None
        self.agro = auto_agro
        self.size = world_size
        if auto_agro:
            self.agro_chance = 0.75
        self.line_break = "=" * 97 + "\n"

    def take_all_items(self):
        """
        takes all items from the current zone and give them to the player
        """
        zone_items = self.world.current_zone.items
        if zone_items:
            for item in zone_items:
                current_item = zone_items.get(item)
                self.player.give_item(current_item)
                if current_item.family == "equipment":
                    print(f"acquired item : {current_item.name}")
                else:
                    print(f"acquired item : {current_item.species}")
            self.world.current_zone.empty_items()
            print("all items acquired")
            self.player.add_move()
        else:
            print("no items to take")

    def get_help(self):
        """
        gets help text for a quest.
        """
        return player.current_quest.help_text        

    def fetch_quest_complete(self):
        """
        checks if the current quest fetch quest is complete.
        """
        if self.current_quest.goal in self.player.inventory:
            return self.current_quest.win()

    def rescue_quest_complete(self):
        """
        checks if the current quest rescue quest is complete.
        """
        if self.current_quest.goal.free:
            return self.current_quest.win()             

    def quest_complete(self):
        switch = {"<class 'FetchQuest'>": fetch_quest_complete, "<class 'RescueQuest'>": rescue_quest_complete}
        case = str(type(self.player.current_quest))
        switch.get(case)()

    def attack(self, attacker, target):
        """
        makes 'attacker' attack 'target' where they are both character 
        subclasses.
        """
        print(self.line_break)
        damage = round(round((attacker.get_atk() / 2) + 0.1) - (round((attacker.get_atk() / 2) + 0.1) * target.stats.get("def")))
        target.damage(damage)
        print(f"\n{attacker} did {damage}, points of damage to {target}\n{self.line_break}")
        print(f"{target}, has {target.current_health} health remaining\n\n{self.line_break}")    
        if not target.alive:
            self.world.current_zone.remove_enemy(target)

    def get_move_order(self):
        """
        generates a turn order for the enemies in the zone and the player.
        """
        enemies = list(self.world.current_zone.enemies)
        char_speed = {enemy.base_stats.get("spe"): enemy for enemy in enemies}
        char_speed.update({self.player.stats.get("spe"): self.player})
        speeds = sorted(char_speed.keys())[::-1]
        order = [char_speed.get(i) for i in speeds]
        return order

    def heal(self, item):
        """
        heals the player with item.
        """
        self.player.use(item)
        
    def make_heading(self):
        """
        it generates a pretty formatted heading.
        :return:
        """
        score = self.player.get_score()
        moves = self.player.get_moves()
        money = self.player.get_money()
        health = self.player.get_health()
        heading = f"{'=' * 97}\n    <:|:>{' ' * 79}<:|:>\n" \
                  f"      |   score  :  {score}{' ' * (70 - len(str(score)))}|\n" \
                  f"      |   moves  :  {moves}{' ' * (70 - len(str(moves)))}|\n" \
                  f"      |   money  :  {money}{' ' * (70 - len(str(money)))}|\n" \
                  f"      |   health :  {health}{' ' * (70 - len(str(health)))}|\n" \
                  f"    <:|:>{' ' * 79}<:|:>\n{self.line_break}\n"
        return heading

    def move(self, direction):
        """
        handle player movement throuh out the world.
        """
        self.player.add_move()
        new_zone = self.world.travel(direction)
        if not new_zone:
            print(self.make_heading() + "Thow, shalt not pass!")
        else:
            print(self.make_heading() + new_zone)
        # if self.agro:
        #     do agro stuff
            
    def spawn_player(self, name=""):
        """
        creates the player character
        """
        if name == "":
            player = ppl.PlayerCharacter()
        else:
            player = ppl.PlayerCharacter(name)
        self.player = player
    
    def add_creature(self, location=(), *creatures):
        """
        makes an npc and adds them to the world in a given location.
        can work of multiple characters as long as they have the same 
        locations and are stored in a list.
        """
        for npc in creatures:
            if type(npc) == ppl.Enemy:
                self.zones[location].add_enemy(npc)
            else:
                self.zones[location].add_npc(npc)

    def add_item(self, location=(), *items):
        """
        will add item to location. can also add mulitle items 
        simultainiously (put the multile items in a, list set, or tuple). 
        """
        for item in items:
            self.zones[location].add_item(item)

    def clean_up_roads(self):
        """
        removes all the connections from zones that haven't been set_up
        """
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                zone = self.zones[row, col]
                if zone.name == f"{row} {col}":
                    zone.conects == zone.default_conects()
                    
    def add_road(self, start, end, direction):
        """
        will add a conection in the directions of 'direction' starting at
        start and ending and 'end'

        start and end are the matrix coordinates that coorespond to the 
        location off the dessiered zone in the np.ndarray, 'self.zones'.
        
        direnction is a one letter lower case string that represnets the
        direction that the player would travel to get from start to end. 
        """
        start.add_conects(direction, end)
        end.add_conects(_opposite_direction(direction), start)  

    def set_zone_text(self, zone, name='d', welcome='d', description='d'):
        """
        sets the name of 'zone' to 'name', the welcome to 'welcome', and
        the description to 'description'.
        if the string of a lower clase 'D', for default, in used as an 
        input for name or welcome that veriable remains the same. 
        """
        if name != "d": 
            self.zones[zone].name = name
        if welcome != "d":
            self.zones[zone].welcome = welcome
        if description != "d":
            self.zones[zone].desc = description
        
    def get_zone_description(self, zone=()):
        """
        returns the description of 'zone'
        is zone is not given this meathod returns teh current zones 
        description.
        """
        if zone == ():
            zone = self.world.current_zone
        else:
            zone = self.zones[(zone)]
        return zone.desc
           
    def _oposite_direction(self, direction):
        """
        helper function
        returns the opposite direction to 'direction'
        """
        opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'nw': 'se', 
                     'ne': 'sw', 'se': 'nw', 'sw': 'ne'}
        return opposites.get(direction)
        
    def _get_slope(self, foo):
        """
        helper function
        returns a string representing the slope of the slope of the line 
        that passes throuugh the two points represneted in foo. with
        ngative and posative numbers represennting the line going in 
        opposite directions.
        """
        directions = {"-1/-1": 'nw', "-1/0": 'n', "-1/1": 'ne', 
                     "0/1": 'e', "1/1": 'se', "1/0": 's', "1/-1": 'sw', 
                     "0/-1": 'w'}
        difference = "/".join([str(j-k) for j, k in foo])
        #print("difference : ", difference)
        direction = directions.get(difference)
        return direction

    def alter_road(self, zone_1=(), zone_2=(), alteration=""):
        """
        used to change or remove roads.
        zone_1 is the startingn zone (similar to 'start' form the 
        add_road meathod.)
        zone_2 is the ending zone (similar to 'end' form the add_road
        meathod.)
        if alteration is left as an empty string the meathod will remove 
        the connection between those two zones.          
        """
        foo = list(zip(zone_2, zone_1))
        if alteration == "":
            direction = self._get_slope(foo)
        else:
            direction = alteration
        oposite = self._oposite_direction(direction)
        #print(f"oposite {oposite}, direction {direction}")
        #print(f"from (z1) {zone_1}, {direction} to (z2) {zone_2}")
        #print(f"from (z2) {zone_2}, {oposite} to (z1) {zone_1}")
        
        self.zones[zone_1].add_conect(direction, self.zones[zone_2])
        self.zones[zone_2].add_conect(oposite, self.zones[zone_1])

    def distribute_objects(self, location=(), objects={}, d_type=""):
        """
        ditributes items or characters to their apropriate zones.
        
        objects is a dictionary where the keys are a tuple representing 
        a matrix coordinate where the object should go

        d_type is a one letter long string the represents the type of 
        object in the dictionary. "c" for "Character" or "i" for "Item"
        and Equipment. 
        """
        d_type = d_type.lower()
        
        if d_type == "c":
            funct = 'self.zones[location].add_npc(ob)'
        elif d_type == "i":
            funct = 'self.zones[location].add_item(ob)'
        elif d_type == "e":
            funct = 'self.zones[location].add_enemy(ob)'
        else:
            print("\n\nfrom class 'game' meathod 'distribute_objects': "
                  "d_type was nither the letter, 'c', nor, 'i', nor, 'e'.")
        #print("objects : ", objects)
        for ob in objects:
            #print(objects.get(loc))
            eval(funct)
    
    def world_setup(self, start_zone, *args):
         """
         run after one edits all the dictionaries. it generates a world 
         object that is made of the stuff with in the dictionaries.  

         start_zone is a tuple the represents the matrix coordinates of 
         the starting zone.

         *args are dictionaries representing the npcs, enemys, and items.
         the keys to all these dictionaries is the a tuple representing the
         location of the value, which would be the object its self.
         """
         for arg in args:
             self.distribute_stuff(arg)
         self.world = world.World(self.zones)
         self.world.set_start(start_zone)

         
    def check_quest_completion(self, quest):
        """
        checks the completion of a quest
        """
        if type(quest) == str:
            for q in self.player.quests:
                if q.name.lower() == quest:
                    return q.complete
        else:
            return quest.complete
