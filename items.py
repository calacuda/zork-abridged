"""
items.py

part of the text-based-rpg progect
this module contains all the items uses the base_items module as a base

By: Calacuda | MIT Licence | Version: Oct 10, 2020
"""


import base_items as bi


class HyperPotion(bi.Potion):
    def __init__(self):
        super().__init__(species="hyper potion", value=100, 
                         regen_amount=10, 
                         description="welcome to the wonderful world of pokemon")
        
