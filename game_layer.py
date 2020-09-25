from typing import Tuple

import api
from game_state import GameState


class GameLayer:
    def __init__(self, api_key):
        self.game_state = None
        self.api_key = api_key
    
    def new_game(self, map_name='training0'):
        game_options = {'mapName': map_name}
        
        self.game_state = GameState(api.new_game(self.api_key, game_options))

    def end_game(self):
        api.end_game(self.api_key, self.game_state.game_id)

    def start_game(self):
        self.game_state.update_state(api.start_game(self.api_key, self.game_state.game_id))

    def place_foundation(self, pos, building_name):
        position = {'X': pos[0], 'Y': pos[1]}
        foundation = {'Position': position, 'BuildingName': building_name}
        self.game_state.update_state(api.place_foundation(self.api_key, foundation, self.game_state.game_id))

    def build(self, pos):
        position = {'position': {'X': pos[0], 'Y': pos[1]}}
        self.game_state.update_state(api.build(self.api_key, position, self.game_state.game_id))

    def maintenance(self, pos):
        position = {'position': {'x': pos[0], 'y': pos[1]}}
        self.game_state.update_state(api.maintenance(self.api_key, position, self.game_state.game_id))

    def demolish(self, pos):
        position = {'position': {'x': pos[0], 'y': pos[1]}}
        self.game_state.update_state(api.demolish(self.api_key, position, self.game_state.game_id))

    def adjust_energy_level(self, pos, value):
        position = {'x': pos[0], 'y': pos[1]}
        self.game_state.update_state(api.adjust_energy(self.api_key, {'position': position, 'value': value}, self.game_state.game_id))

    def wait(self):
        self.game_state.update_state(api.wait(self.api_key, self.game_state.game_id))

    def buy_upgrade(self, pos, upgrade):
        position = {'x': pos[0], 'y': pos[1]}
        self.game_state.update_state(api.buy_upgrades(self.api_key, {'position': position, 'upgradeAction': upgrade}, self.game_state.game_id))

    def get_score(self):
        return api.get_score(self.api_key, self.game_state.game_id)

    def get_game_info(self, game_id):
        self.game_state = GameState(api.get_game_info(self.api_key, game_id))

    def get_game_state(self, game_id):
        self.game_state.update_state(api.get_game_state(self.api_key, game_id))

    def get_blueprint(self, building_name):
        res_blueprint = self.get_residence_blueprint(building_name)

        if res_blueprint:
            return res_blueprint

        return self.get_utility_blueprint(building_name)

    def get_residence_blueprint(self, building_name):
        for blueprint in self.game_state.available_residence_buildings:
            if blueprint.building_name == building_name:
                return blueprint

        return None

    def get_utility_blueprint(self, building_name):
        for blueprint in self.game_state.available_utility_buildings:
            if blueprint.building_name == building_name:
                return blueprint

        return None

    def get_effect(self, effect_name):
        for effect in self.game_state.effects:
            if effect.name == effect_name:
                return effect
        return None
