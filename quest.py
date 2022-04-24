"""
quest.py

part of the python based text based adventure game project contains the 
quest objects.

By: Calacuda | MIT Licence | Epoch: Oct 22, 2019
"""


class Quest:
    def __init__(self, name, description, reward, win_conditions):
        self.name = name
        self.description = description
        self.reward = reward
        self.win_conditions = win_conditions
        self.complete = False
        self.help_text = ""

    def __str__(self):
        return f"{self.name}:\nself.description\n"

    def set_help_text(self, text):
        self.help_text = text

    def win(self):
        """
        activate when the player has met the win condition this will 
        mark the quest as completed.
        """
        self.complete = True
        return self.reward

    def get_status(self):
        """
        returns weather or not the quest is complete
        """
        return self.complete
        

class FetchQuest(Quest):
    def __init__(self, name, description, reward, goal_item):
        super().__init__(name=name, description=description, reward=reward, win_conditions=goal_item)
        self.goal = goal_item


class RescueQuest(Quest):
    def __init__(self, name, description, reward, person):
        super().__init__(name=name, description=description, reward=reward, win_conditions=person)
        self.person = person
        
