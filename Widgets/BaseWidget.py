from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from plyer import notification
from EncryptionUtility import EncryptionUtility
from Utilities.JsonHelper import JsonHelper
from Utilities.StringCollection import ToolMode
from pyperclip import copy

class BaseWidget(Screen):
    main_color = ListProperty((0.55, 0.88, 0.95, 1))
    darker_color = ListProperty((0.043, 0.054, 0.070, 1))
    user_input = ObjectProperty(None)
    output_result = ObjectProperty(None)
    encryptor_btn = ObjectProperty(None)

    encryptor_tool = None
    saved_config = None

    json_helper = JsonHelper()

    def on_pre_enter(self, *args):
        Clock.schedule_once(self._load_settings_deferred, 0)

    def load_settings(self):
        self.saved_config = self.json_helper.read_config()

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