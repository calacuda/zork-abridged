"""
sound.py

plays music and sound effects in a background process.


By: Calacuda | MIT Licence | Epoch: May 5th, 2020
"""


import os
import vlc
import time
from multiprocessing import Process


class Song:
    def __init__(self, file_path):
        self.path = os.getcwd() + "/sounds/" + file_path

    def __iter__(self):
        return self

    def __next__(self):
        return self.path


class Music:
    def __init__(self, fname):
        self.fname = fname
        self.media = Song(fname)
        self.player = Process(target=self._que_sound, args=())
        self.player.start()

    def play(self, fname):
        self.fname = fname
        self.media = Song(fname)
        self.player.terminate()
        self.player = Process(target=self._que_sound, args=())
        self.player.start()
        
    def stop(self):
        self.player.terminate()

    def _que_sound(self):
        sound = self.media
        for song in sound:
            vlc_instance = vlc.Instance()
            player = vlc_instance.media_player_new()
            media = vlc_instance.media_new(song)
            player.set_media(media)
            player.play()
            time.sleep(1.5)
            duration = (player.get_length() / 1000) - 2
            time.sleep(duration)
