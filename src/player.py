import json
from CONSTANTS import *

class Player():
    def __init__(self, default_data: dict) -> None:
        self.default_data = default_data # Default data
        
        # Live data
        self.money = self.default_data["starting_money"]
        self.fuel = self.default_data["starting_fuel"]
        self.magnet_radius = self.default_data["magnet_radius"]
        self.minimap_radius = self.default_data["minimap_radius"]
        self.upgrades = self.default_data["upgrades"]

        self.deaths = 0
    
    """ def update_data(self) -> dict:
        self.data["starting_money"] = self.starting_money
        self.data["starting_fuel"] = self.starting_fuel
        self.data["magnet_radius"] = self.magnet_radius
        self.data["minimap_radius"] = self.minimap_radius
        self.data["upgrades"] = self.upgrades
        return self.data """
    
    def load_data(self) -> dict:
        state = 2 # Everything loaded correctly
        reasons = []
        
        try:
            with open(PATH + "/save_data.json", "r") as f:
                save_data = json.load(f)
        except:
            save_data = {}
            state = 0
            reasons.append("FILENOTFOUND")

            self.money = self.default_data["starting_money"]
            self.fuel = self.default_data["starting_fuel"]
            self.magnet_radius = save_data["magnet_radius"]
            self.minimap_radius = self.default_data["minimap_radius"]
            self.upgrades = self.default_data["upgrades"]
            self.deaths = 0

            return {state: reasons}

        try:
            self.money = save_data["money"]
        except KeyError:
            self.money = self.default_data["starting_money"]
            state = 1
            reasons.append("money")


        try:
            self.fuel = save_data["fuel"]
        except KeyError:
            self.fuel = self.default_data["starting_fuel"]
            state = 1
            reasons.append("fuel")

        try:
            self.magnet_radius = save_data["magnet_radius"]
        except KeyError:
            self.magnet_radius = self.default_data["magnet_radius"]
            state = 1
            reasons.append("magnet_radius")

        try:
            self.minimap_radius = save_data["minimap_radius"]
        except KeyError:
            self.minimap_radius = self.default_data["minimap_radius"]
            state = 1
            reasons.append("minimap_radius")

        try:
            self.upgrades = save_data["upgrades"]
        except KeyError:
            self.upgrades = self.default_data["upgrades"]
            state = 1
            reasons.append("upgrades")

        try:
            self.deaths = save_data["deaths"]
        except KeyError:
            self.deaths = 0
            state = 1
            reasons.append("deaths")

        return {state: reasons}

    def save_data(self) -> bool:
        data = {"money": self.money,
                "fuel": self.fuel,
                "magnet_radius": self.magnet_radius,
                "minimap_radius": self.minimap_radius,
                "upgrades": self.upgrades,
                "deaths": self.deaths}
        with open(PATH + "/save_data.json", "w") as f:
            json.dump(data, f, ensure_ascii=True, indent=4)
        

        