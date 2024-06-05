import json
from CONSTANTS import *

class Player():
    def __init__(self, default_data: dict) -> None:
        self.default_data = default_data # Default data
        
        # Live data
        self.money = self.default_data["money"]
        self.fuel_level = self.default_data["fuel_level"]
        self.starting_fuel = self.default_data["starting_fuel"]
        self.starting_speed = self.default_data["starting_speed"]
        self.magnet_level = self.default_data["magnet_level"]
        self.map_level = self.default_data["map_level"]
        self.max_speed_level = self.default_data["max_speed_level"]

        self.deaths = 0
    
    def load_data(self) -> dict:
        state = 1 # Everything loaded correctly
        reasons = []
        
        try:
            with open(PATH + "/save_data.json", "r") as f:
                save_data = json.load(f)
        except:
            save_data = {}
            state = 0
            reasons.append("FILENOTFOUNDORCORRUPTED")

            self.money = self.default_data["money"]
            self.fuel_level = self.default_data["fuel_level"]
            self.starting_fuel = self.default_data["starting_fuel"]
            self.starting_speed = self.default_data["starting_speed"]
            self.magnet_level = self.default_data["magnet_level"]
            self.map_level = self.default_data["map_level"]
            self.max_speed_level = self.default_data["max_speed_level"]
            self.deaths = 0
            return {state: reasons}

        self.money = save_data["money"]
        self.fuel_level = save_data["fuel_level"]
        self.starting_fuel = save_data["starting_fuel"]
        self.starting_speed = save_data["starting_speed"]
        self.magnet_level = save_data["magnet_level"]
        self.map_level = save_data["map_level"]
        self.max_speed_level = save_data["max_speed_level"]
        self.deaths = save_data["deaths"]
        return {state:[]}

    def save_data(self) -> bool:
        data = {"money": self.money,
                "fuel_level": self.fuel_level,
                "starting_fuel": self.starting_fuel,
                "starting_speed": self.starting_speed,
                "magnet_level": self.magnet_level,
                "map_level": self.map_level,
                "max_speed_level": self.max_speed_level,
                "deaths": self.deaths}
        with open(PATH + "/save_data.json", "w") as f:
            json.dump(data, f, ensure_ascii=True, indent=4)
        

        