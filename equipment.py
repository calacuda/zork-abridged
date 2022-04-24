"""
equipment.py

part of the text-based-rpg project.
this module holds the the non base equipment classes

By: Calacuda | MIT Licence | Epoch: Oct 10, 2019 |
"""


import base_equipment as be


class BambooSword(be.Weapon):
    def __init__(self):
        super().__init__(species="sword", name="bamboo sword", value=5,
                         score=1, damage=7, mag_damage=2, 
                         description="it's a babmoo sparing sword")

class DirtSword(be.Weapon):
    def __init__(self):
        super().__init__(species="sword", name="foam sword", value=2,
                         score=1, damage=3, mag_damage=1, 
                         description="its a sword made of foam, what "
                                     "did you expect")
        
class Excalibur(be.Weapon):
    def __init__(self):
        super().__init__(species="sword", name="excalibur", value=10,
                         score=10, damage=10, mag_damage=30, 
                         description="the holy weapon made famous by "
                                     "King Arther in Arthurian legends.")
