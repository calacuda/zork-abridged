"""
equipment.py

python 3.6

part of the python based text based adventure game project and contains the equipment objects.

By: Calacuda | MIT Licence | Epoch: ?
"""


import base_items as items


class Equipment(items.Item):
    def __init__(self, genus, species, name, value, score, durability=25, description=""):
        super().__init__(family="equipment", genus=genus, species=species, value=value, score=score,
                         description=description)
        self.name = name
        self.durability = durability
        self.actions.update({"damage": self.reduce_durability})

    def __str__(self):
        return f"{self.name}: {self.species}, {self.description}"

    def __repr__(self):
        return self.__str__()

    def reduce_durability(self, amount=1):
        self.durability -= amount
        if self.durability <= 0:
            self._break()
            return "i'm broken, please fix me"

    def _break(self):
        self.value = 0
        self.stats = True


class Weapon(Equipment):
    """
    This is all weapons. kind is type of weapon, bows, staffs, swords, daggers, wands, axes, etc. all else is handled in
    the 'Item' class.
    """
    def __init__(self, species, name, value, score, damage, mag_damage, description=""):
        super().__init__(genus="weapon", species=species, name=name, value=value, score=score)
        self.damage = damage
        self.mag_damage = mag_damage
        self.actions.update({"attack": self.damage, "atk": self.damage})
        if not description:
            self.description = f"This is {name}, it is a {species}."
        else:
            self.description = description

    def get_power(self):
        return self.damage


class Armor(Equipment):
    def __init__(self, species, name, value, score, catagory, defence=0, mag_def=0, description="Just a piece of armor,"
                                                                                                "nothing special"):
        super().__init__(genus="armor", species=species, name=name, value=value, score=score, description=description)
        # self.durability = durability
        self.defence = defence
        self.mag_def = mag_def
        self.catagory = catagory

    def get_def(self):
        return self.defence

    def get_mag_def(self):
        return self.mag_def


# class Msc(Armor):
#     def __init__(self, species, name, value, score, defence=0, mag_def=0, description=""):
#         super().__init__(genus= "armor", species)
