import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class MoreWidgets(Widget):
    def on_enter(self):
        print("name: ", self.name.text)
        self.name.text = ""

class KivyPlayground(App):
    def build(self):
        return MoreWidgets()


KivyPlayground().run()
