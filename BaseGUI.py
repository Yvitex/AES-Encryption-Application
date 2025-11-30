import os

from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from EncryptionUtility import EncryptionUtility

from plyer import notification
from pyperclip import copy
from kivy.clock import Clock
from Utilities.StringCollection import ToolMode

window_width = 590
window_height = 730

Config.set('graphics', 'width', window_width)
Config.set('graphics', 'height', window_height)

from kivy.app import App
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
import json

config_path = "./assets/configuration.json"

main_color = ListProperty((0.55, 0.88, 0.95, 1))
darker_color = ListProperty((0.043, 0.054, 0.070, 1))

# This function reads the config data if there is
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

# The home screen of the app
class BaseWidget(Screen):
    main_color = ListProperty((0.55, 0.88, 0.95, 1))
    darker_color = ListProperty((0.043, 0.054, 0.070, 1))
    user_input = ObjectProperty(None)
    output_result = ObjectProperty(None)
    encryptor_btn = ObjectProperty(None)

    encryptor_tool = None
    saved_config = None

    def on_enter(self):
        Clock.schedule_once(self._load_settings_deferred, 0)

    def load_settings(self):
        self.saved_config = read_config()

        if self.saved_config is not None:
            if self.saved_config.get("iv", "") is None:
                notification.notify("Reminder", "You do not have an IV key yet, set it on settings")
            elif self.saved_config.get("secret_key", "") is None:
                notification.notify("Reminder", "You do not have an IV key yet, set it on settings")
            else:
                self.encryptor_tool = EncryptionUtility(self.saved_config["secret_key"].encode(),
                                                    self.saved_config["iv"].encode())

            if self.saved_config.get("mode", "") == ToolMode.EncryptionMode:
                self.ids.encryptor_btn.text = "Encrypt"
            elif self.saved_config.get("mode", "") == ToolMode.DecryptionMode:
                self.ids.encryptor_btn.text = "Decrypt"
            else:
                self.ids.encryptor_btn.text = "Encrypt"


    def _load_settings_deferred(self, dt):
        self.load_settings()


    # When you press the setting icon, it will go to the settings page with this function
    def go_to_settings(self):
        manager = self.manager
        manager.transition.direction = "left"
        manager.current = "setting"

        setting_screen = manager.get_screen("setting")
        # get the instance of the setting page, from there, we can modify the content of the textbox

        if self.saved_config is not None:
            if 'iv' in setting_screen.ids and 'secret_key' in setting_screen.ids:
                setting_screen.ids.iv.text = self.saved_config.get("iv", "")
                setting_screen.ids.secret_key.text = self.saved_config.get("secret_key", "")
                setting_screen.ids.mode_button.text = self.saved_config.get("mode", "")

    def unified_encrypt_decrypt(self):
        if self.encryptor_tool is None:
            notification.notify("Reminder", "You haven't set your settings yet", timeout=5)
            return
        if self.saved_config is not None:
            if self.saved_config.get("mode", "") == ToolMode.EncryptionMode:
                self.encrypt()
            elif self.saved_config.get("mode", "") == ToolMode.DecryptionMode:
                self.decrypt()
        else:
            self.encrypt()


    # Yes this is the encrypt function
    def encrypt(self):
        result = self.encryptor_tool.encrypt_aes(self.user_input.text)
        self.output_result.text = result
        notification.notify("AES Encryptor", "Output copied to clipboard", timeout=3)
        copy(result)

    # Decrypt function
    def decrypt(self):
        result = self.encryptor_tool.decrypt_aes(self.user_input.text)
        self.output_result.text = result
        notification.notify("AES Encryptor", "Output copied to clipboard", timeout=3)
        copy(result)




# The settings screen
class SettingWidget(Screen):
    main_color = ListProperty((0.55, 0.88, 0.95, 1))
    darker_color = ListProperty((0.043, 0.054, 0.070, 1))

    secret_key = ObjectProperty(None)
    iv = ObjectProperty(None)
    secret_key_label = ObjectProperty(None)
    iv_label = ObjectProperty(None)

    mode_button = ObjectProperty(None)
    selected_mode = ToolMode.EncryptionMode

    # We get the configuration data and turn them to json
    def save_setting(self):
        # validate the input
        validated = self.validate_iv_secret()
        if validated:

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
            self.go_to_base()

    # this function allows you to go to base from settings
    def go_to_base(self):
        manager = self.manager
        manager.transition.direction = "right"
        manager.current = "base"

        # and then we reload the settings from the base so it will use updated data
        base_screen = manager.get_screen("base")
        base_screen.load_settings()


    # This changes the selected button of the dropdown
    def update_mode_button(self, mode):
        self.selected_mode = mode
        if self.mode_button:
            self.mode_button.text = mode

    def create_dropdown(self):
        dropdown = DropDown()
        modes = [ToolMode.EncryptionMode, ToolMode.DecryptionMode]

        for mode in modes:
            btn = Button(text=mode, size_hint_y=None, height=50, background_normal="", background_color=self.darker_color)
            btn.bind(on_release=lambda drop_btn: dropdown.select(drop_btn.text))
            dropdown.add_widget(btn)

        dropdown.bind(on_select=lambda instance, x: self.update_mode_button(x))
        return dropdown

    # this handles the validation of the secret key and iv, if there's an error, outputs text
    def validate_iv_secret(self):
        validated_secret = False
        validated_iv = False

        if len(self.secret_key.text) is not 16:
            self.secret_key_label.text = "The Secret Key should be 16 characters long"
        else:
            validated_secret = True
            self.secret_key_label.text = ""

        if len(self.iv.text) is not 16:
            self.iv_label.text = "The IV should be 16 characters long"
        else:
            validated_iv = True
            self.iv_label.text = ""

        if validated_secret is False or validated_iv is False:
            return False
        else:
            return True


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file(filename="./basegui.kv")

class BaseGUI(App):
    def build(self):
        Window.clearcolor = (0.055, 0.067, 0.086, 1)
        Window.size = (window_width, window_height)
        return kv


