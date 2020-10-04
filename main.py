import colorama
import glob
import os

from datetime import datetime
from json import load
from sys import argv

from game_layer import GameLayer
from strategy import Strategy

colorama.init()

api_key = ''

with open('super.secret') as f:
    api_key = f.readline().rstrip()

map_name = 'training'

game_layer = GameLayer(api_key)

def write(filename, commands):
    with open(filename, 'w') as f:
        for command in commands:
            if command[-1] != '\n':
                command = command + '\n'
            f.write(command)

def play(commands):
    timestring = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'games\\{map_name}-{timestring}-{game_layer.game_state.game_id}.dump'  

    print('Done with game: ' + game_layer.game_state.game_id)
    print('Final score was: ' + str(game_layer.get_score()['finalScore']))
    
    write(filename, commands)

def simple():
    game_layer.new_game(map_name)
    print('Starting', 'simple game:', game_layer.game_state.game_id)
    game_layer.start_game()  

    commands = []
   
    while game_layer.game_state.turn < game_layer.game_state.max_turns:
        commands.append(take_turn())

    play(commands)

def simple2():
    strategy_settings = None
    
    with open(f'simple2_{map_name}.json') as f:
        strategy_settings = load(f)

    games = 200

    for game in range(games):    
        game_layer.new_game(map_name)

        print('Starting', 'simple2 game:', game_layer.game_state.game_id)
        game_layer.start_game()
        strategy = Strategy(game_layer.game_state, strategy_settings)

        for residence in game_layer.game_state.residences:
            game_layer.game_state.map[residence.X][residence.Y] = 1
            strategy.building_counts[residence.building_name] += 1

        for utility in game_layer.game_state.utilities:
            game_layer.game_state.map[utility.X][utility.Y] = 1
            strategy.building_counts[utility.building_name] += 1

        commands = []
    
        while game_layer.game_state.turn < game_layer.game_state.max_turns:
            command = take_turn2(strategy)
            commands.append(command)
            
            game_layer.translate(command.split())
            # print(game_layer.game_state)

        # print(game_layer.game_state)
        print(f'Game: {game+1}/{games}')
        play(commands)

def replay(filename):
    game_layer.new_game(map_name)
    print('Starting', 'replay game:', game_layer.game_state.game_id)
    game_layer.start_game()  

    commands = []

    with open(filename) as f:
        commands.append(f.readline())

    play(commands)

def play_recorded(name=''):
    recordings = glob.glob('/games/*')

    if not recordings:
        die('No available games!')
    else:
        if not name:
            replay(max(recordings, key=os.path.getctime))
        else:
            if name not in recordings:
                die('Game not found!')
            else:
                replay(name)


def die(message=''):
    print('Fatal. Exiting. ' + message)


def record():
    pass #TODO


def interactive():
    game_layer.new_game(map_name)
    print('Starting', 'interactive game:', game_layer.game_state.game_id)
    game_layer.start_game()
    print(game_layer.game_state)
    print()

    commands = []
   
    while game_layer.game_state.turn < game_layer.game_state.max_turns:
        s = ''

        while not game_layer.validate(s):
            s = input()

        game_layer.translate(s.split())
        print(colorama.ansi.clear_screen())
        print(game_layer.game_state)

    play(commands)


def endall():
    games = game_layer.get_games()
    print('Ending active games.')
    
    for game in games:
        if game['active']:
            game_layer.end_game(game['gameId'])
            print('Ended', game['gameId'])

def main():
    global map_name

    if len(argv) < 2:
        die('Supply command!')
        return

    mode = argv[1]

    endall()

    if len(argv) == 2:
        die('Supply map number!')
    else:        
        map_number = argv[2]
        map_name += map_number

        if mode == 'simple':
            simple()
        elif mode == 'latest':
            play_recorded()
        elif mode == 'named':
            if len(argv) < 3:
                die('Missing parameter: Name')
            else:
                play_recorded(argv[2])
        elif mode == 'record':
            record()
        elif mode == 'interactive':
            interactive()        
        elif mode == 'simple2':
            simple2()
        else:
            die('Unknown command')

def take_turn():
    state = game_layer.game_state

    command = ''

    x = -1
    y = -1

    maxrescount = 3

    if len(state.residences) < maxrescount:
        for i in range(len(state.map)):
            if x > -1:
                break
            for j in range(len(state.map[i])):
                if state.map[i][j] == 0:
                    x = i
                    y = j
                    break

        command = game_layer.place_foundation((x, y), game_layer.game_state.available_residence_buildings[0].building_name)
    else:
        building = False

        for residence in state.residences:
            if residence.build_progress < 100:
                command = game_layer.build((residence.X, residence.Y))
                building = True
                break

        if not building:
            healing = False
            
            for residence in state.residences:
                if residence.health < 30:
                    command = game_layer.maintenance((residence.X, residence.Y))
                    healing = True
                    break

            if not healing:
                command = game_layer.wait()

    for message in game_layer.game_state.messages:
        print(message)
    for error in game_layer.game_state.errors:
        print('Error: ' + error)

    return command


def take_turn2(strategy):
    state = game_layer.game_state

    if strategy.demolished:
        x, y = strategy.demolished
        strategy.building_counts['HighRise'] += 1
        strategy.demolished = None
        return f'place_foundation {x} {y} HighRise'

    for residence in state.residences:
        if residence.build_progress < 100:
            return f'build {residence.X} {residence.Y}'

    for utility in state.utilities:
        if utility.build_progress < 100:
            return f'build {utility.X} {utility.Y}'

    for residence in state.residences:
        if residence.health < strategy.repair_limit and strategy.should_repair(residence.building_name):
            return f'maintenance {residence.X} {residence.Y}'

    adjustee = strategy.most_urgent_energy_changee()

    if adjustee:
        energy_level, base_energy_need, current_level = strategy.adjust_energy(adjustee)

        strategy.energy_adjustments[(adjustee.X, adjustee.Y)] = state.turn

        new_level = energy_level if energy_level > base_energy_need else base_energy_need + (current_level - base_energy_need) * strategy.temperature_undershoot_bounce

        return f'adjust_energy_level {adjustee.X} {adjustee.Y} {new_level}'

    upgrade, x, y = strategy.upgrade_suggestion()

    if upgrade:
        return f'buy_upgrade {residence.X} {residence.Y} {upgrade}'

    if state.funds >= strategy.purchase_threshold:
        for _, cost, name, x, y in strategy.build_choice():
            if cost > state.funds:
                break

            if x >= 0:
                strategy.build_order_pos += 1
                return f'place_foundation {x} {y} {name}'

            if name not in state.releases or state.releases[name] > state.turn:
                continue

            if not state.available_spaces():
                break
            
            x, y = strategy.build_place(name)

            if x == -1:
                continue

            strategy.building_counts[name] += 1
            
            return f'place_foundation {x} {y} {name}'

    if strategy.earliest_demolish <= state.turn <= strategy.latest_demolish and state.funds >= strategy.demolish_fund_limit and strategy.building_counts['HighRise'] < strategy.highrise_limit and state.housing_queue >= strategy.demolishing_queue_limit:
        if strategy.building_counts['Apartments'] > 1:
            for residence in state.residences:
                if residence.building_name == 'Apartments':
                    strategy.building_counts['Apartments'] -= 1
                    strategy.demolished = (residence.X, residence.Y)

                    return f'demolish {residence.X} {residence.Y}'
    
    return 'wait'


if __name__ == '__main__':
    main()
