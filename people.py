"""
people.py

python 3.6

part of the python based text based adventure game project contains the objects to create text based RPG characters.

By: Calacuda | MIT Licence | Epoch: ?
"""

from math import inf
import items
import equipment as equip

bamboo_sword = equip.BambooSword()
dirt_sword = equip.DirtSword()


class Character:
    def __init__(self, name, job, immortality):
        self.name = name
        self.job = job.lower() if job != None else job
        self.inventory = []
        self.alive = True
        self.money = 0
        self.base_stats = {"hlth": 0, "str": 0, "def": .0, "mag_str": 0, "mag_def": 0, "spe": 0}
        self.equipment = {"weapon": None, "shield": None, "helmet": None, "body": None,
                          "legs": None, "arms": None, "hands": None}
        self.stats = self.base_stats.copy()
        if immortality:
            self.stats["hlth"] = inf
        self.current_health = self.stats.get("hlth")
        self.alive = True

    def __str__(self):
        return self.name + ", " + self.stats.__repr__()

    def use(self, item):
        item = {item}.intersection(self.inventory)
        item = item.pop()
        affects = item.use()
        if item.genus == "buffs":
            old_stat = self.stats.get(affects[0])
            self.stats[affects[0]] *= affects[1]
            param = self.stats[affects[0]] - old_stat
        elif item.genus == "potion":
            old_health = self.get_health()
            hlth = self.stats.get("hlth") + affects
            if hlth >= self.base_stats.get("hlth"):
                self.full_heal()
            else:
                self.stats["hlth"] += affects
            self.hlth_update()
            param = self.get_health() - old_health
        else:
            print("ERROR")
        if item.uses >= 0:
            self.inventory.remove(item)
        return item.use_text(param)

    def get_item(self, name_or_kind):
        for posesion in self.inventory:
            if posesion.family == "equipment":
                if (name_or_kind == posesion.species) or (name_or_kind == posesion.name):
                    return posesion
            else:  # i.e if possesion is an item that isnt equipment like a consumable.
                if (name_or_kind == posesion.species) or (name_or_kind == posesion.genus):
                    return posesion
        return 0.0

    def inventory_membership_test(self, item):
        flag = False
        for posesion in self.inventory:
            if posesion.family == "equipment":
                flag = flag or (item == posesion.species) or (item == posesion.name)
            else:
                flag = flag or (item == posesion.species) or (item == posesion.genus)
        return flag

    def set_base_stats(self, health=-inf, strength=-inf, defence=-inf, mag_str=-inf, mag_def=-inf, speed=-inf):
        new_stats = (health, strength, defence, mag_str, mag_def, speed)
        counter = 0
        for stat in self.base_stats:
            if new_stats[counter] > -1:
                self.base_stats[stat] = new_stats[counter]
            counter += 1

    def stat_restore(self):
        """
        restores stats to their base values but does not heal.
        :return:
        """
        self.hlth_update()
        self.stats = self.base_stats
        self.stats["hlth"] = self.current_health

    def full_heal(self):
        self.stats = self.base_stats
        self.hlth_update()

    def damage(self, amount):
        new_health = self.stats["hlth"] - amount
        if new_health <= 0:
            self.stats["hlth"] = 0
            self.alive = False
        else:
            self.stats["hlth"] = new_health
        self.hlth_update()

    def hlth_update(self):
        self.current_health = self.stats.get("hlth")
        if self.current_health <= 0:
            self.alive = False

    def take_item(self, item):
        self.inventory = {possession for possession in self.inventory if possession != item}

    def take_money(self, amount):
        self.money -= amount

    def give_money(self, amount):
        self.money += amount

    def set_name(self, new_name):
        self.name = new_name

    def get_atk(self):
        return self.stats.get("str")

    def get_inventory(self):
        return self.inventory

    def get_money(self):
        return self.money

    def get_name(self):
        return self.name

    def get_health(self):
        return self.stats.get("hlth")


class PlayerCharacter(Character):
    def __init__(self, name="Chuckles"):
        super().__init__(name, "adventurer", False)
        self.score = 0
        self.moves = 0
        self.title = "The Awakened One"
        self.base_stats = {"hlth": 20, "str": 5, "def": .02, "mag_str": 2, "mag_def": .01, "spe":  2}
        self.equipment = {"weapon": bamboo_sword, "shield": None, "helmet": None, "body": None,
                          "legs": None, "arms": None, "hands": None}
        self.stats = self.base_stats.copy()
        self.hlth_update()
        self.quests = {}
        self.current_quest = None

    def __str__(self):
        return str(self.name) + ", " + str(self.title)

    def add_quest(self, *quests):
        """
        adds a quest to self.quests. uses the quest name as a key and the
        quest as a value
        """
        if self.current_quest == None:
            self.current_quest = quests[0]
        for quest in quests:
            self.quests.update({quest.name: quest})

    def set_current_quest(self, quest):
        """
        sets the currrent quest to quest
        """
        if type(quest) == str:
            self.current_quest = self.quests.get(quest)
        else:
            self.current_quest = quest
    
    def equip(self, equipment):
        try:
            family = equipment.family
            if family != "equipment":
                print("that's not equipment!")
                return
            else:
                # switch = {"weapon": self._equip_weapon, "helmet": self._equip_helmet, "body": self._equip_body,
                #           "legs": self._equip_legs, "arms": self._equip_arms, "hands": self._equip_hands}
                if equipment.genus.lower() == "weapon":
                    old_equipment = self._equip_weapon(equipment)
                    category = "weapon"
                else:
                    category = equipment.species
                    old_equipment = self._equip_armor(equipment, category)
                self.inventory.remove(equipment)
                self.equipment[category] = equipment
                self.inventory.append(old_equipment)
        except UnboundLocalError:
            print(":P")

    def _equip_weapon(self, weapon):
        old_weapon = self.equipment.get("weapon")
        self.stats["str"] -= old_weapon.damage
        self.stats["mag_str"] -= old_weapon.damage
        self.stats["str"] += weapon.mag_damage
        self.stats["mag_str"] += weapon.mag_damage
        return old_weapon

    def _equip_armor(self, armor, kind):
        old_armor = self.equipment.get(kind.lower())
        self.stats["def"] -= old_armor.defence
        self.stats["mag_def"] -= old_armor.mag_def
        self.stats["def"] += armor.defence
        self.stats["mag_def"] += armor.mag_def
        return old_armor

    def set_title(self, title):
        self.title = title

    def give_item(self, item):
        self.inventory.append(item)
        self.score += item.score

    def add_move(self):
        self.moves += 1

    def get_moves(self):
        return self.moves

    def get_score(self):
        return self.score


class NPC(Character):
    def __init__(self, name, job, immortality=True, quest=None):
        super().__init__(name=name, job=job, immortality=immortality)
        self.money = inf
        self.quest = quest


class CaptivePrinces(NPC):
    def __init__(self, name="Jolene"):
        super().__init__(name=name, job="princes", immortality=True)
        self.free = False

    def set_free(self):
        self.free = True
    

class CaptiveNPC(NPC):
    def __init__(self, name, job, importality=True):
        super().__init__(name=name, job=job, imortality=imortality)
        self.free = False

        
class Enemy(Character):
    def __init__(self, name="Rymaru", species="slime", job="Leader", imortality=False):
        super().__init__(name=name, job=job, immortality=imortality)
        self.species = species.lower()
        self.base_stats = {"hlth": 15, "str": 3, "def": .01, "mag_str": 1, "mag_def": .009, "spe": 1}
        self.money = round(sum(self.base_stats.values()) + 0.1)
        self.equipment = {"weapon": dirt_sword, "shield": None, "helmet": None, "body": None,
                          "legs": None, "arms": None, "hands": None}
        self.stats = self.base_stats.copy()
        self.drops = {drop for drop in self.equipment.values() if drop is not None}

    def __str__(self):
        return self.name

