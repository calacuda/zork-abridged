# zork-abridged
A set of python scripts to make text based adventure games with. It includes a sameple game ("Zork Abridged", A.K.A "Xork")


### ~~~
### Intro:
### ~~~

This project is a python program that makes a text based adventure game. It
is writen in Python3 (originally 3.6, but 3.7, 3.8 also work).


### ~~~
### running a sample game:
### ~~~

simply run main.py. to reset the sample game, run builder and enter "yes"
to the two prompts. to make your own game see the using section below.


### ~~~
### using:
### ~~~

one simply needs to edit a few json files or make you're own versions of 
the json files with the same names.


### ~~~
### Files:
### ~~~


### * game.py.bak:

A backup of the game file


### * test.py:

A file to test ideas during developement.


### * dev-docs.txt:

notes about the development of this game by and for its developers. 
(eg. TODO's, design notes, etc.)


### * params.json

contains all the data about zones, enemies, items, and the like, edit this to edit the game. 

### * builder.py:

This program builds the game object then stores it as a file in the same 
folder. Go here to change anything about the game world but not the 
the engine. For exmple, you can change the script, modifie items and 
locations that kind of stuff.


### * game.py:

This file contains the game object. it is used by builder and only builder
to create the game_engine.pickle file.


### * engine.pickle:

The file where the base game file is stored. This is NOT a user save file


### * save_1.pickle:

Is the default save file.


### * base_quest.py:

Holds the quest objects used in the creation of the quests for the game.


### * base_equipment.py:

Holds the base equpiment objects (weapons, armor, etc). Used to create 
equipment classes for equipment that apears more then once in the game.


### * base_items:

Base item objects (Item, Consumable, etc). Used to create classes for 
items used more then once in the game. 


### * equipment.py:

One object for all commen pieses of equipment in the world.


### * items.py:

Same deal as equipment but for items.


### * enemies.py

Contanis common enemies classes.


### * people.py

Contains all the people objects (PlayerCharacter, NPC, Character, etc).


### * main.py:

The file one runs to play the game. uses the game_engine.pickle file and 
the players save file.
