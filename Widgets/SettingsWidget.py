from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from Utilities.StringCollection import ToolMode
from Utilities.JsonHelper import JsonHelper
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import os
import json

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

    json_helper = JsonHelper()

    def on_pre_enter(self, *args):
        if 'iv' in self.ids and 'secret_key' in self.ids:
            saved_config = self.json_helper.read_config()
            if saved_config is not None:
                self.ids.iv.text = saved_config.get("iv", "")
                self.ids.secret_key.text = saved_config.get("secret_key", "")
                self.ids.mode_button.text = saved_config.get("mode", "")

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

            os.makedirs(os.path.dirname(self.json_helper.config_path), exist_ok=True)

            try:
                with open(self.json_helper.config_path, "w") as json_file:
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