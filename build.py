"""
build.py 

reads a json file and builds a world based on that data. 

By: Calacuda | MIT Licence | Epoch: May 4th, 2020 | version: epoch
"""


import json
import pickle
import game
from people import *
from enemies import *
from items import *
from equipment import *
from base_quests import *


fname = "params.json"
f = open(fname)
data = json.load(f)
f.close()
engine = game.Game("the lands of lowderouse", (2, 2))
engine_name = "engine.pickle"
save_file = "save_1.pickle"



def make_player(params):
    """
    makes and returns a player object
    """
    player = PlayerCharacter()
    if params:
        for key in params.keys():
            val = params.get(key)
            eval(f"player.{key} = {val}")
    return player
    

def make_zone(params):
    """
    makes a zone
    """
    engine.set_zone_text(tuple(params.get("location")), params.get("name"), params.get("welcome"), params.get("description"))


def generate_zones(zones):
    """
    calls make_zone on all the zones
    """
    for zone in zones:
        make_zone(zone)


def make_a_thing(params):
    """
    returns and item of the secifications
    """
    try:
        return eval(f"{params.get('name').replace(' ', '')}()")
    except:
        print("that item doesn't exsist yet")
        print(params)


def distribute_things(things):
    """
    makes the items and puts them in the specified location
    """
    for params in things:
        engine.distribute_objects(tuple(params.pop("location")), {make_a_thing(params),}, params.get("type"))


def save():
    """
    make two pickle files one is an engine and the other is a default save file.
    """
    engine.clean_up_roads()
    f = open(engine_name, 'wb')
    pickle.dump(engine, f)
    f.close()
    f = open(save_file, 'wb')
    pickle.dump(engine, f)
    f.close()    
    
        
def mod_roads(loc_1, loc_2, direction):
    """
    changes form teh default north, south, east, west, to up, down, or whatever 
    loc_1 = location 1
    loc_2 = location 2
    direction = direction from loc_1 to loc_2, ie what you would type after 'go' to get from loc_1 to loc_2
    """
    pass



def populate(params):
    """
    makes npcs and puts them in the world.
    """
    pass

    

def main():
    engine.spawn_player(make_player(data.pop("player")))
    generate_zones(data.pop("zones"))
    distribute_things(data.pop("items"))
    distribute_things(data.pop("enemies"))
    distribute_things(data.pop("NPCs"))
    engine.world_setup((1,1))
    save()


if __name__ == "__main__":
    main()
