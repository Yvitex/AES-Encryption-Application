import os

from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from EncryptionUtility import EncryptionUtility

window_width = 590
window_height = 730

Config.set('graphics', 'width', window_width)
Config.set('graphics', 'height', window_height)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
import json

config_path = "./assets/configuration.json"

main_color = ListProperty((0.55, 0.88, 0.95, 1))
darker_color = ListProperty((0.043, 0.054, 0.070, 1))

def read_config():
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as json_file:
                json_data = json.load(json_file)
            return json_data

        except Exception as e:
            print(e.message)
            return None
    else:
        return None

class BaseWidget(Screen):
    main_color = ListProperty((0.55, 0.88, 0.95, 1))
    darker_color = ListProperty((0.043, 0.054, 0.070, 1))
    user_input = ObjectProperty(None)
    output_result = ObjectProperty(None)
    saved_config = read_config()

    if saved_config != None:
        encryptor_tool = EncryptionUtility(saved_config["secret_key"].encode(), saved_config["iv"].encode())
    else:
        print("Set an encryption key and iv in the tool settings")

    def encrypt(self):
        result = self.encryptor_tool.encrypt_aes(self.user_input.text)
        self.output_result.text = result


class SettingWidget(Screen):
    main_color = ListProperty((0.55, 0.88, 0.95, 1))
    darker_color = ListProperty((0.043, 0.054, 0.070, 1))

    secret_key = ObjectProperty(None)
    iv = ObjectProperty(None)

    mode_button = ObjectProperty(None)
    selected_mode = "Encryption Mode"


    def save_setting(self):
        new_config = {
            "secret_key": self.secret_key.text,
            "iv": self.iv.text,
            "mode": self.selected_mode,
        }

        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        try:
            with open(config_path, "w") as json_file:
                json.dump(new_config, json_file, indent=4)
        except Exception as e:
            print(e.message)


    def update_mode_button(self, mode):
        self.selected_mode = mode
        if self.mode_button:
            self.mode_button.text = mode

    def create_dropdown(self):
        dropdown = DropDown()
        modes = ["Encryption Mode", "Decryption Mode"]

        for mode in modes:
            btn = Button(text=mode, size_hint_y=None, height=50, background_normal="", background_color=self.darker_color)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        dropdown.bind(on_select=lambda instance, x: self.update_mode_button(x))
        # self.mode_button.text = "Mode: " + self.selected_mode
        return dropdown


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file(filename="./basegui.kv")


class BaseGUI(App):
    def build(self):
        Window.clearcolor = (0.055, 0.067, 0.086, 1)
        Window.size = (window_width, window_height)
        return kv


