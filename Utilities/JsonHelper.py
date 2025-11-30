import os
import json



class JsonHelper:
    config_path = "./assets/configuration.json"

    # This function reads the config data if there is
    def read_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as json_file:
                    json_data = json.load(json_file)
                return json_data

            except Exception as e:
                print(e.message)
                return None
        else:
            return None