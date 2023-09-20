from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class AiVideoGenerator(App):
    def build(self):
        
        layout =  BoxLayout(orientation = 'vertical', spacing = 10, padding = 40)
        textinput = TextInput(text='Hello world', size_hint=(1, 0.9))
        btn1 = Button(text = "Generate Video", size_hint=(1, 0.1))
        layout.add_widget(textinput)
        layout.add_widget(btn1)
        return layout

AiVideoGenerator().run()    