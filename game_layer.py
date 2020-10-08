from api import Api
from game_state import GameState


class GameLayer:
    def __init__(self, api_key):
        self.game_state = None
        self.api = Api(api_key)

    def translate(self, instruction):
        command = instruction[0]

        if command == 'wait':
            return self.wait()

        pos = [int(instruction[1]), int(instruction[2])]
        
        if command == 'place_foundation':
            return self.place_foundation(pos, instruction[3])
        if command == 'build':
            return self.build(pos)
        if command == 'maintenance':
            return self.maintenance(pos)
        if command == 'demolish':
            return self.demolish(pos)
        if command == 'adjust_energy_level':
            return self.adjust_energy_level(pos, float(instruction[3]))
        if command == 'demolish':
            return self.demolish(pos)
        return self.buy_upgrade(pos, instruction[3])

    def validate(self, s):
        if not s:
            return False

        instruction = s.split()

        command = instruction[0]

        if command == 'wait':
            return True

        if command not in ('place_foundation', 'build', 'maintenance', 'demolish', 'adjust_energy_level', 'buy_upgrade'):
            return False

        if len(instruction) < 3:
            return False

        if not instruction[1].isdigit() or not instruction[2].isdigit():
            return False

        if command in ('place_foundation', 'buy_upgrade'):
            return len(instruction) == 4

        if command == 'adjust_energy_level':
            if len(instruction) != 4:
                return False
            try:
                float(instruction[3])
                return True
            except:
                return False
        return True
    
    def new_game(self, map_name='training0'):
        game_options = {'mapName': map_name}
        
        self.game_state = GameState(self.api.new_game(game_options))
        self.api.set_game_id(self.game_state.game_id)

    def end_game(self, game_id=''):
        param = game_id if game_id else self.game_state.game_id
        self.api.end_game(param)

    def start_game(self):
        self.game_state.update_state(self.api.start_game(self.game_state.game_id))

    def place_foundation(self, pos, building_name):
        position = {'X': pos[0], 'Y': pos[1]}
        foundation = {'Position': position, 'BuildingName': building_name}

        self.game_state.map[pos[0]][pos[1]] = 1
        self.game_state.update_state(self.api.place_foundation(foundation, self.game_state.game_id))

        return f'place_foundation {pos[0]} {pos[1]} {building_name}\n'

    def build(self, pos):
        position = {'position': {'X': pos[0], 'Y': pos[1]}}
        self.game_state.update_state(self.api.build(position, self.game_state.game_id))

        return f'build {pos[0]} {pos[1]}\n'

    def maintenance(self, pos):
        position = {'position': {'x': pos[0], 'y': pos[1]}}
        self.game_state.update_state(self.api.maintenance(position, self.game_state.game_id))

        return f'maintenance {pos[0]} {pos[1]}\n'

    def demolish(self, pos):
        position = {'position': {'x': pos[0], 'y': pos[1]}}
        self.game_state.update_state(self.api.demolish(position, self.game_state.game_id))

        return f'demolish {pos[0]} {pos[1]}\n'

    def adjust_energy_level(self, pos, value):
        position = {'x': pos[0], 'y': pos[1]}
        self.game_state.update_state(self.api.adjust_energy({'position': position, 'value': value}, self.game_state.game_id))

        return f'adjust_energy_level {pos[0]} {pos[1]} {value}\n'

    def wait(self):
        self.game_state.update_state(self.api.wait(self.game_state.game_id))

        return 'wait\n'

    def buy_upgrade(self, pos, upgrade):
        position = {'x': pos[0], 'y': pos[1]}
        self.game_state.update_state(self.api.buy_upgrades({'position': position, 'upgradeAction': upgrade}, self.game_state.game_id))

        return f'buy_upgrade {pos[0]} {pos[1]} {upgrade}\n'

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