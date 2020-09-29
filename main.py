import colorama
import glob
import os

from sys import argv
from time import time

from game_layer import GameLayer

colorama.init()

api_key = ''

with open('super.secret') as f:
    api_key = f.readline().rstrip()

# The different map names can be found on considition.com/rules
map_name = 'training1'  # TODO: You map choice here. If left empty, the map 'training1' will be selected.

game_layer = GameLayer(api_key)


def write(filename, commands):
    with open(filename, 'w') as f:
        for command in commands:
            f.write(command)

def play(commands):
    filename = f'games\\{map_name}-{str(time()).split(".")[0]}'  

    print('Done with game: ' + game_layer.game_state.game_id)
    print('Final score was: ' + str(game_layer.get_score()['finalScore']))

    game_layer.end_game()
    
    write(filename, commands)

def simple():
    game_layer.new_game(map_name)
    print('Starting', 'simple game:', game_layer.game_state.game_id)
    game_layer.start_game()  

    commands = []
   
    while game_layer.game_state.turn < game_layer.game_state.max_turns:
        commands.append(take_turn())

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
    if len(argv) < 2:
        die('Supply command!')
    else:
        mode = argv[1]

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
        elif mode == 'endall':
            endall()
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
        # elif residence.health < 50:
        #     command = game_layer.maintenance((residence.X, residence.Y))
        # elif residence.temperature < 18:
        #     blueprint = game_layer.get_residence_blueprint(residence.building_name)
        #     energy = blueprint.base_energy_need + 0.5 \
        #              + (residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
        #              - residence.current_pop * 0.04
        #     command =  game_layer.adjust_energy_level((residence.X, residence.Y), energy)
        # elif residence.temperature > 24:
        #     blueprint = game_layer.get_residence_blueprint(residence.building_name)
        #     energy = blueprint.base_energy_need - 0.5 \
        #              + (residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
        #              - residence.current_pop * 0.04
        #     command = game_layer.adjust_energy_level((residence.X, residence.Y), energy)
        # elif state.available_upgrades[0].name not in residence.effects:
        #     command =  game_layer.buy_upgrade((residence.X, residence.Y), state.available_upgrades[0].name)
        # else:
        #     command = game_layer.wait()

    for message in game_layer.game_state.messages:
        print(message)
    for error in game_layer.game_state.errors:
        print('Error: ' + error)

    return command

if __name__ == '__main__':
    main()
