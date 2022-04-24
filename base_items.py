"""
items.py

python 3.6

part of the python based text based adventure game project and contains the item objects.

By: Calacuda | MIT Licence | Epoch: ?
"""

potion_score = 5
buff_score = 15


class Item:
    """
    this class includes all items, potions, weapons and equipment, quest items, basically any thing that a character
    could logically hold in their inventory.
    """
    def __init__(self, family, genus, species, value, score=0, description=""):
        self.family = family
        self.genus = genus
        self.species = species
        self.value = value
        self.score = score
        self.name = species
        if not description:
            self.description = f"This is {family}, it is a {genus} of type {species}."
        else:
            self.description = description
        self.actions = {"appraise": self.value, "info": self.description}

    def __str__(self):
        return f"{self.species}: {self.genus}, {self.description}"

    def __repr__(self):
        return self.__str__()

    def get_value(self):
        return self.value

    def get_actions(self):
        return self.actions

    def get_species(self):
        return self.species

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name


class Potion(Item):
    """
    healing items.
    """
    def __init__(self, species, value, regen_amount, description=""):
        super().__init__(family="consumables", genus="potion", species=species, value=value, score=potion_score)
        self.regen_amount = regen_amount
        self.uses = 1
        self.actions.update({"use": self.use})
        if not description:
            self.description = f"This is a {species}, it is a healing item and heals {regen_amount} points of damage."
        else:
            self.description = description

    def __str__(self):
        return f"{self.species}: {self.genus} it heals {self.regen_amount}."

    def __repr__(self):
        return self.__str__()

    def use(self):
        self.uses -= 1
        return self.regen_amount

    def use_text(self, amount_healed):
        return f"the {self.species} healed, {amount_healed} points of damage"


class Buffs(Item):
    """
    buffing items that increases a specific or multiple stats.
    """
    def __init__(self, species, value, stat, boost, description):
        super().__init__(family="consumables", genus="buffs", species=species, value=value, score=buff_score)
        self.stat = stat
        self.boost = boost
        self.uses = 1
        self.actions.update({"use": self.use})
        if not description:
            self.description = f"This is a {species}. It boosts {stat} by {boost} points."
        else:
            self.description = description

    def __str__(self):
        return f"{self.species}, {self.genus}: it boost {self.stat} by {self.boost}"

    def __repr__(self):
        return self.__str__()

    def use(self):
        self.uses -= 1
        return self.stat, self.boost

    def use_text(self, amount_buffed):
        return f"the {self.species} buffed, {self.boost} points of damage"
