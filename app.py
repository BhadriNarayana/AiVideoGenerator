from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
import time

from kivy.uix.videoplayer import VideoPlayer


Builder.load_file('app.kv')

class ScreenOne(Screen):
    def generate(self):
        self.manager.current = "second"

class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        video_player = VideoPlayer(source="FinalOne.mp4")
        self.add_widget(video_player)

class AiVideoGenerator(App):
    def build(self):
        sm = ScreenManager()
        one = ScreenOne(name = "first")
        two = ScreenTwo(name = "second")
        sm.add_widget(one)
        sm.add_widget(two)
        return sm

AiVideoGenerator().run()    