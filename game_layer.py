from api import Api
from game_state import GameState


class GameLayer:
    def __init__(self, api_key):
        self.game_state = None
        self.api = Api(api_key)
    
    def new_game(self, map_name='training0'):
        game_options = {'mapName': map_name}
        
        self.game_state = GameState(self.api.new_game(game_options))

    def end_game(self, game_id=''):
        param = game_id if game_id else self.game_state.game_id
        self.api.end_game(param)

    def start_game(self):
        self.game_state.update_state(self.api.start_game(self.game_state.game_id))

    def place_foundation(self, pos, building_name):
        position = {'X': pos[0], 'Y': pos[1]}
        foundation = {'Position': position, 'BuildingName': building_name}
        self.game_state.update_state(self.api.place_foundation(foundation, self.game_state.game_id))

        return 'place_foundation ' + building_name

    def build(self, pos):
        position = {'position': {'X': pos[0], 'Y': pos[1]}}
        self.game_state.update_state(self.api.build(position, self.game_state.game_id))

        return 'build ' + str(pos[0]) + ',' + str(pos[1])

    def maintenance(self, pos):
        position = {'position': {'x': pos[0], 'y': pos[1]}}
        self.game_state.update_state(self.api.maintenance(position, self.game_state.game_id))

        return 'maintenance' + str(pos[0]) + ',' + str(pos[1])

    def demolish(self, pos):
        position = {'position': {'x': pos[0], 'y': pos[1]}}
        self.game_state.update_state(self.api.demolish(position, self.game_state.game_id))

        return 'demolish' + str(pos[0]) + ',' + str(pos[1])

    def adjust_energy_level(self, pos, value):
        position = {'x': pos[0], 'y': pos[1]}
        self.game_state.update_state(self.api.adjust_energy({'position': position, 'value': value}, self.game_state.game_id))

        return 'adjust_energy_level' + str(pos[0]) + ',' + str(pos[1])

    def wait(self):
        self.game_state.update_state(self.api.wait(self.game_state.game_id))

        return 'wait'

    def buy_upgrade(self, pos, upgrade):
        position = {'x': pos[0], 'y': pos[1]}
        self.game_state.update_state(self.api.buy_upgrades({'position': position, 'upgradeAction': upgrade}, self.game_state.game_id))

        return 'buy_upgrade' + str(pos[0]) + ',' + str(pos[1]) + upgrade

    def get_score(self):
        return self.api.get_score(self.game_state.game_id)

    def get_game_info(self, game_id):
        self.game_state = GameState(self.api.get_game_info(game_id))

    def get_game_state(self, game_id):
        self.game_state.update_state(self.api.get_game_state(game_id))

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

    def get_games(self):
        return self.api.get_games()