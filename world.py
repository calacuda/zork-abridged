"""
world building.py

python 3.6

part of the python based text based adventure game project and contains the objects necessary to create a text based RPG
world.

By: Calacuda | MIT Licence | Epoch: ?
"""
line_break = "=" * 97


class Zone:
    def __init__(self, name, welcome=""):
        self.name = name
        self.desc = ""
        self.welcome = welcome
        self.conects = self.default_conects()
        self.items = {}
        self.npcs = set(())
        self.enemies = set(())
        self.sound = None
        # self.move_order =

    def __str__(self):
        return self.name + "\n\n" + self.welcome

    def default_conects(self):
        cant_go_there = 'there a sign that says, "Construction in progress. We appreciate your patients." with a \n' \
                        'picture of some god awful post modern building that looks like it was designed by an \n' \
                        'arthritic 4 y/o with a crayon. So you will have to find another way!'
        conects = {"n": cant_go_there, "s": cant_go_there, "e": cant_go_there, "w": cant_go_there,
                        "u": cant_go_there, "d": cant_go_there, "nw": cant_go_there, "ne": cant_go_there,
                        "sw": cant_go_there, "se": cant_go_there,}
        return conects

    def get_move_order(self, player):
        """
        generates a turn order for the enemies in the zone and the player.
        :param player_speed:
        :return:
        """
        order = []
        char_speed = {player.stats.get("spe"): player}
        enenemy = list(self.enemies)
        for enemy in enenemy:
            char_speed.update({enemy.base_stats.get("spe"): enemy})
        speeds = set((char_speed.keys()))
        temp_speeds = speeds.copy()
        for speed in speeds:
            fastest = max(temp_speeds)
            temp_speeds.remove(fastest)
            order.append(char_speed.get(fastest))
        return order

    def take_item(self, name_or_kind):
        for possesion in self.items:
            if self.items.get(possesion).family == "consumables":
                if ((name_or_kind == self.items.get(possesion).genus) or
                   (name_or_kind == self.items.get(possesion).species)):
                    acquisition = self.items.pop(possesion)
                    break
            elif self.items.get(possesion).family == "equipment":
                if ((name_or_kind == self.items.get(possesion).name) or
                   (name_or_kind == self.items.get(possesion).species)):
                    acquisition = self.items.pop(possesion)
                    break
        try:
            return acquisition
        except UnboundLocalError:
            print("i dont have that item.")

    def get_item(self, name_or_kind):
        for possesion in self.items:
            if self.items.get(possesion).family == "consumables":
                if ((name_or_kind == self.items.get(possesion).genus) or
                   (name_or_kind == self.items.get(possesion).species)):
                    acquisition = self.items.get(possesion)
                    break
            elif self.items.get(possesion).family == "equipment":
                if ((name_or_kind == self.items.get(possesion).name) or
                   (name_or_kind == self.items.get(possesion).species)):
                    acquisition = self.items.get(possesion)
                    break
        try:
            return acquisition
        except UnboundLocalError:
            print("i dont have that item.")

        # for name_or_kind in self.items:
        #     if name_or_kind == name_or_kind:
        #         acquisition = self.items.get(name_or_kind)
        #         self.items.take_item(name_or_kind)
        #         self.items.take_item(name_or_kind)
        #         return acquisition

    def item_membership_test(self, item):
        flag = False
        for possesion in self.items:
            if self.items.get(possesion).family == "consumables":
                flag = flag or ((item == self.items.get(possesion).genus) or
                                (item == self.items.get(possesion).species))
            elif self.items.get(possesion).family == "equipment":
                flag = flag or ((item == self.items.get(possesion).name) or
                                (item == self.items.get(possesion).species))
        return flag

    def enemy_membership_test(self, test_enemy):
        flag = False
        for enemy in self.enemies:
            flag = flag or ((test_enemy == enemy.name) or
                            (test_enemy == enemy.species))
        return flag

    def get_enemy(self, name_or_kind):
        for enemy in self.enemies:
            if (name_or_kind == enemy.name) or (name_or_kind == enemy.species):
                return enemy

    def empty_items(self):
        self.items.clear()

    def set_desc(self, desc):
        self.desc = desc

    def set_name(self, name):
        self.name = name

    def set_welcome(self, welcome):
        self.welcome = welcome

    def add_conect(self, direction, zone):
        self.conects[direction] = zone

    def add_enemy(self, enemy):
        self.enemies.add(enemy)

    def add_npc(self, npc):
        self.npcs.add(npc)

    def add_item(self, *items):
        for item in items:
            self.items.update({item.get_name(): item})

    def get_items(self):
        return self.items

    def get_name(self):
        return self.name

    def get_desc(self):
        return self.desc

    def get_welcome(self):
        return self.welcome

    def get_conects(self):
        return self.conects

    def remove_enemy(self, enemy):
        self.enemies = {e for e in self.enemies if e != enemy}

    def remove_conect(self, direction):
        del self.conects[direction]


class World:
    def __init__(self, zones):
        self.opposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e", "u": "d", "d": "u"}
        self.zones = zones
        #self.current_zone = self.zones[0]
        self.current_zone = None

    def travel(self, direction):
        direction = direction.lower()[0]
        connections = self.current_zone.get_conects()
        if (direction in connections) and (type(self.current_zone.get_conects().get(direction)) != str):
            # if type(self.current_zone.get_conects().get(direction)) != str:
            self.current_zone = self.current_zone.get_conects().get(direction)
            if len(self.current_zone.enemies) > 0:
                enemies = "\n".join(['    ' + str(enemy) for enemy in self.current_zone.enemies])
                zone = str(self.current_zone) + f"\n\nthere's evil afoot! \n{enemies}"
            else:
                zone = str(self.current_zone)
            return zone
        else:
            return False

    def add_zone(self, *zones):
        for zone in zones:
            self.zones.append(zone)

    def add_road(self, origin_zone, direction, destination_zone):
        origin_zone.add_conects(direction, destination_zone)
        destination_zone.add_conects(self.opposite_directions.get(direction), origin_zone)

    def get_zones(self):
        return self.zones

    def get_location(self):
        return self.current_zone

    def set_start(self, location=()):
        """
        sets the starting location of the world
        """
        if len(location) != 2:
            # make self.current_zone the middle of the map.
            shape = self.zones.shape
            location = (int(shape[0] / 2), int(shape[1] / 2)) 
        self.current_zone = self.zones[location]
