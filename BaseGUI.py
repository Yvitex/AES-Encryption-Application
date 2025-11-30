
from kivy.config import Config

window_width = 590
window_height = 730

Config.set('graphics', 'width', window_width)
Config.set('graphics', 'height', window_height)

from kivy.app import App
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder

from Widgets.BaseWidget import BaseWidget
from Widgets.SettingsWidget import SettingWidget

main_color = ListProperty((0.55, 0.88, 0.95, 1))
darker_color = ListProperty((0.043, 0.054, 0.070, 1))

class WindowManager(ScreenManager):
    pass

Builder.load_file(filename="./WidgetKV/BaseKV.kv")
Builder.load_file(filename="./WidgetKV/SettingsKV.kv")

kv_manager = Builder.load_file(filename="./WidgetKV/WidgetManager.kv")


class BaseGUI(App):
    def build(self):
        Window.clearcolor = (0.055, 0.067, 0.086, 1)
        Window.size = (window_width, window_height)
        return kv_manager


