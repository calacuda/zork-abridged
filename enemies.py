"""
enemies.py

part of the text-based-rpg progect.
this module holds all the enemy objects, orc, troll, goblin, etc.

By: Calacuda | MIT Licence | Version: Oct 10th, 2020
"""


import people as ppl
import items as ite
import equipment as equip


class Orc(ppl.Enemy):
    def __init__(self, name="orc", species="orc", job="unemployed", imortality=False):
        super().__init__(name=name, species=species, job=job, imortality=imortality)
        self.set_base_stats(speed=3)

class Troll(ppl.Enemy):
    def __init__(self, name="troll", species="troll", job="unemployed", imortality=False):
        super().__init__(name=name, species=species, job=job, imortality=imortality)


class Goblin(ppl.Enemy):
    def __init__(self, name="goblin", species="goblin", job="unemployed", imortality=False):
        super().__init__(name=name, species=species, job=job, imortality=imortality)
            

class Dragon(ppl.Enemy):
    def __init__(self, name="Puff", species="dragon", job="unemployed", imortality=False):
        super().__init__(name=name, species=species, job=job, imortality=imortality)

    def __str__(self):   
        return f"{self.name} the {self.species}"     
