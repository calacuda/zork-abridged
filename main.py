"""
main.py

part of the the text-based-rpg project.
the main file for the text-based-rpg project. it is resposible for 
lenguage parsing and switch boarding comands.

By: Calacuda | MIT Licence | Epoch: Oct 11, 2019 |
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from random import random                                             
import sound

stop_words = set(stopwords.words('english'))
words = {"attack": 'vb', "atk": 'vb', "take": "vb", "heal": "vb", "loot": "vb", "go": "vb",
         "north": 'n', "south": 'n', "east": 'n', "west": 'n', "save": 'vb', "load": 'vb',
         "loot": 'vb', "use": 'vb', "look": 'vb', "equip": 'vb', "check": 'vb',
         "quest": 'vb'}
cmd_spec_args = {"equipment": 'n', "stats": 'n', "items": 'n', 
                 "inventory": 'n', "quests": 'n', #"equip": 'n', 
                 "equiped": 'n', "complete": 'n', "status": 'n',
                 "set": 'n',}
    

def load(command):
    """
    loads a pickled game file
    """
    fname = input("name a save file to load, default is 'save_1.pickle'\n    <:|:> ")
    if fname.strip() == "":
        fname = "save_1.pickle"
    f = open(fname, 'rb')
    global engine
    engine = pickle.load(f)
    f.close()  
    print(f" - loaded save file {fname} - ")


def save(command):
    """
    pickles the game object to a file of the users choosing.
    """
    fname = input("name you save file, default is 'save_1.pickle'\n    <:|:> ")
    if fname.strip() == "":
        fname = "save_1.pickle"
    f = open(fname, 'wb')
    pickle.dump(engine, f)
    f.close()    
    print(f" - saved to file {fname} - ")


def args_error():
    """
    prints a generic error message if the arguments input by the user dont make sence.
    """
    print("What you talkin' bout' Willis?!")
    

def check(command):
    """
    will print the information about the player outlined in command.
    e.g if command says equipment then check() will print the players 
    equipment, etc.
    """
    if len(args.debug.intersection({"all", 'check'})):
        print(f"check({command})")
    for word, pos in command:
        if word in ["equipment", "equip", "equiped"]:
            print("Equipment:\n")
            for kind, equipment in engine.player.equipment.items():
                try:
                    print(f"{kind} :  {equipment.name}")
                except AttributeError:
                    print(f"{kind} :  {None}")
        elif word == "items" or word == "inventory":
            print("Items:\n")
            for item in engine.player.inventory:
                print("*", item)
        elif word == "stats":
            print("Stats:\n")
            for stat, val in engine.player.stats.items():
                print(f"{stat} :  {val} / {engine.player.base_stats.get(stat)}")
        elif word == "quests":
            print("Quests:\n")
            quests = engine.player.quests
            for quest in quests:
                print(f"* {quest} :\n{quests.get(quest).description}")            


def quest(command):
    """
    handles questing stuff
    """
    num_quests = len(engine.player.quests)
    if num_quests > 0:
        current_quest = engine.player.current_quest
        # print("current quest : ", current_quest)
        # complete = current_quest.complete
        complete = engine.check_quest_completion(current_quest)
        for word, pos in command:
            if word == "complete" and complete:
                engine.quest_complete()
            elif word == "complete" and not complete:
                print("Not sure if you've noticed, but you havent completed that quest yet... so thats a thing.")
            elif word == "set":
                set_quest()
            elif word == "status":
                print(f"The quest {current_quest.name} is {'complete' if complete else 'incomplete'}")
    elif num_quests == 0:
        print("You haven't accepted any quests yet... *cough* coward *cough*. What? I didn't say that.")
    if len(command) == 0:
        print("ya kinda need to tell me what you want me to do. like, I'm grasping at straws here")
        
            
def quest_complete():
    """
    completes the current quest
    """
    # print("quest_complete called")
    reward = engine.quest_complete()
    if type(reward) == int:
        engine.player.money += reward
    else:
        engine.player.give_item(reward)


def set_quest(command):
    """
    sets the players current quest to a quest of the players choosing  
    """
    quests = tuple(engine.player.quests)
    print("Quests:\n")
    for i in range(len(quests)):
        q = quests[i]
        done = engine.check_quest_completion(q)
        print(f"({i}): [{'x' if done else ' '}] {q.name}")
    selection = int(input("which quest would you like to select?\n\t<:|:>"))
    engine.player.set_current_quest(quests[selection])
    

def equip(command):
    """
    finds the equipment object and equips in on the player  
    """
    if len(args.debug.intersection({"all", 'equip'})):
        print(f"equip({command})")
    equip_names = [item.name for item in engine.player.inventory if item.family == "equipment"]
    for word, pos in command:
        if word in equip_names:
            equipment = engine.player.get_item(word)
            engine.player.equip(equipment)
            print(f"{engine.player}, just equiped {equipment}... well, arn't they special...")
          

def go(command):
    """
    sends the player in 'direction' 
    """
    if len(args.debug.intersection({"all", 'go'})):
        print(f"go({command})")
    directions = ["north", "south", "east", "west", "n", "s", "e", "w"]
    for word, pos in command:
        if pos == 'n' and word in directions:
            direction = word
    try:
        old_sound = engine.world.current_zone.sound
        engine.move(direction)
        new_sound = engine.world.current_zone.sound
        if new_sound != old_sound:
            BKG_MUSIC.play(new_sound)
        # print(engine.make_heading())
        # print(engine.world.current_zone)
    except UnboundLocalError:
        cmd = [i[0] for i in command]
        print("no where in that jargen was there a direction.")


def loot(command): 
    """
    takes all items form current_zone and give them to player.
    command is there for stability
    """
    engine.take_all_items()    


def look(command):
    """
    prints the description of the current zone.
    command is there for stability
    """
    text = str(engine.world.current_zone)
    if engine.world.current_zone.desc:
        text += ' ' + engine.world.current_zone.desc
    print(text)


def heal(command):
    """
    auto heals the player.
    """
    print("not programmed yet")
    
    
def use(comand):
    """
    uses an item in the players inventory and applies its effects
    :param comand:
    :return:
    """
    if len(args.debug.intersection({'all', 'use'})):
        print(f"use({comand})")
        # print(f"engine.player.inventory : ", engine.player.inventory)
    old_health = engine.player.current_health
    for word, pos in comand:
        if len(args.debug.intersection({'all', 'use'})):
            print(engine.player.inventory_membership_test(word))
        if engine.player.inventory_membership_test(word):
            print(f"using item: {word}")
            item = engine.player.get_item(word)
            print(engine.player.use(item))
            print(engine.line_break)
        elif pos != 'vb':
            print(f"I do not know the meaning of the word, '{word}'.")
        else:
            print(f"'{word}', is a command not an item.")
            

def attack(command):
    """
    calls engine.atttack(target) where target is the target from command.
    """
    if len(args.debug.intersection({'all', 'attack'})):
        print(f"attack({command})")
    for word, pos in command:
        if pos == "pn":
            target = word
        elif word in engine.player.inventory and engine.player.inventory.get(word).family == "equipment":
            engine.player.equip(player.items.get(word))
    for enemy in  engine.world.current_zone.enemies:
        if enemy.name == target:
            target = enemy
            break
    if len(args.debug.intersection({'all', 'attack'})):
        print("target : ", target)
    try:
        engine.attack(engine.player, target)
    except UnboundLocalError:
        print("Watch where your swinging that thing! Do you even have a target in mind?") 
    if not target.alive:
        print(f"{engine.player}, defeated {target}!")
    

def word_split(sentence):
    """
    will split word sentence in to words. two word proper nouns will be 
    one entry.
    """
    if len(args.debug.intersection({'all', 'word_split'})):
        print(f"word_split({sentence})", type(sentence))
    temp_words = words.copy()
    for enemy in engine.world.current_zone.enemies:
        temp_words.update({enemy.name.lower(): "pn"})
    for item in engine.world.current_zone.items:
        temp_words.update({item: "n"})
    for npc in engine.world.current_zone.npcs:
        temp_words.update({npc.name.lower(): "pn"})
    for item in engine.player.inventory:
        temp_words.update({item.name: "n"})
    temp_words.update(words)
    if len(args.debug.intersection({'all', 'word_split'})):
        print("temp_words : ", temp_words)
    items = engine.player.inventory + list(engine.world.current_zone.items.keys())
    enemies = engine.world.current_zone.enemies
    parsed = []
    for i in range(len(sentence)):
        try:
            phrases = tuple((sentence[i], sentence[i] + " " + sentence[i+1]))            
        except IndexError:
            phrases = tuple([sentence[i]])
        #if args.debug:
        #    print("phrases : ", phrases)        
        for phrase in phrases:
            if phrase in temp_words:
                entry = (phrase, temp_words.get(phrase))
            if phrase in cmd_spec_args:
                entry = (phrase, cmd_spec_args.get(phrase))
        try:
            #if args.debug:
            #    print("entry :", entry)
            if entry not in parsed:
                parsed.append(entry)
                if len(args.debug.intersection({'all', 'word_split'})):            
                    print(f"appending {entry} to parsed")
        except UnboundLocalError:
            args_error()
    if len(args.debug.intersection({'all', 'word_split'})):
        print("parsed : ", parsed)
    return parsed


def pre_prossesing(command):
    """
    parses 'command'
    """
    if len(args.debug.intersection({'all', 'pre_prossesing'})):
        print(f"pre_prossesing({command})", type(command))
    index_counter = 0
    for word, part_of_speach in command:
        if part_of_speach == 'vb':
            index = index_counter
        index_counter += 1
    try:
        if index > 0:
            command[index], command[0] = command[0], command[index]
    except:
        print("I sence that you have no actions in your command. Try again.")
        return             
    if len(args.debug.intersection({'all', 'pre_prossesing'})):
        print("command", command)
    return command


def get_cmd():
    """
    returns the  users command.
    """
    command = input("\n<:|:>  ").lower()
    while not command:
        command = input("\n<:|:>  ").lower()
    if command == "quit":
        answer = input("are you sure you want to leave?\n    <:|:>  ").lower()
        if answer in ["yes", "y"]:
            print("Thank you for playing!")
            BKG_MUSIC.stop()
            exit()
        else:
            print("i'll take that as a no")
    return command            


def switch(in_battle=False):
    """
    battle defines what the legal moves at a point in the game are. if 
    in battle, player cant, loot, save, look, etc.
    """
    if in_battle:
        legal_moves = ("attack", "heal", "use", "equip", "run")    
    else:
        legal_moves = [word for word in words if words.get(word) == 'vb' and word != 'run']
    if len(args.debug.intersection({'all', 'switch'})):
        print("legal_moves : ", legal_moves)
    prossesed_cmd = [("foobar", "slang")]
    while prossesed_cmd != None and prossesed_cmd[0][0] not in legal_moves:
        command = get_cmd().split()
        command = [word for word in command if word not in stop_words]
        command = word_split(command)
        prossesed_cmd = pre_prossesing(command)
        if len(args.debug.intersection({'all', 'switch'})):
            print("prossesed_cmd : ", prossesed_cmd)            
    try:
        funct = prossesed_cmd[0][0]  # the verb input by the user
        if len(args.debug.intersection({'all', 'switch'})):
            print("funct : ", funct)
        eval(funct+f"(prossesed_cmd[1:])")
    except TypeError:
        pass
    
            
def main():
    last_zone = engine.world.current_zone
    while True:
        if not engine.player.alive:
            print("you lost to : ")
            for enemy in engine.world.current_zone.enemies:
                print("    |> ", enemy)
            print("bru... get gud\n\nbut like for real though")
            print("\n\n")
            break
        #elif engine.current_zone.enemies and round(random(), 2) < agro_chance:
        #    battle_switch()
        else:
            if (engine.world.current_zone.enemies and round(random(), 2) < engine.agro_chance): # (engine.world.current_zone != last_zone) and 
                while engine.world.current_zone.enemies:
                    for actor in engine.get_move_order():
                        if actor == engine.player:
                            switch(True)                        
                        else:
                            engine.attack(actor, engine.player)
                            if not engine.player.alive:
                                print(f"OOF! you died.")
                                print(f"you lost to {actor}.")
                                print("\n\nGAME OVER!\n\n")
                                print("Thanks for playing!")
                            enemies_num = len(engine.world.current_zone.enemies)
                        if len(engine.world.current_zone.enemies) != enemies_num:
                            break
            else:
                switch(False)
            last_zone = engine.world.current_zone        
    print("Thanks for playing!")


if __name__ == "__main__":
    import sys
    import argparse
    import pickle

    parser = argparse.ArgumentParser(description="you're goin on an adventure! use '-l' or '--load' "
                                                 "to followed by the name of your save file ot load "
                                                 "an old game")
    parser.add_argument("-l", "--load", dest="engine", default="engine.pickle", type=str)
    parser.add_argument("-d", "--debug", dest="debug", default='', type=str, nargs='+')
    args = parser.parse_args()
    args.debug = set(args.debug)
                                                                                            
    try:
        engine = pickle.load(open(args.engine, 'rb'))
    except FileNotFoundError:
        while True:
            fname = input("please enter a the right filename with the '.pickle' file extention: ")
            right_file = input(f"Is this, '{fname}' the right file name? ")
            if right_file.lower() in ['y', 'yes']:
                print(" - understood - ")
                engine = pickle.load(open(fname, 'rb'))
                break
    print(f"{engine.line_break}\n"
          f"Welcome to Xork! The totally legit, totally not a rip off of Zork, and totally amazing game. also, no Xork"
          f"\n"
          f"does not use the word totally too much. We here at the <Big Tree Games> writing staff, or BTGWS for short,"
          f"\n"
          f"also know how commas work and do not use them in place of periods, \n\n"
          f"That Legal Junk no one Reads:\n\n"
          f"Zork is a registered trade mark of infocom.inc all rights reserved. please support the official release."
          f"\n\n"
          + engine.make_heading() +
          f"{engine.world.get_location()}")
    BKG_MUSIC = sound.Music(engine.world.current_zone.sound)    
    main()
