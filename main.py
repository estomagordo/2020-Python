import glob
import os

from sys import argv
from time import time

from game_layer import GameLayer

api_key = ''

with open('super.secret') as f:
    api_key = f.readline().rstrip()

# The different map names can be found on considition.com/rules
map_name = 'training1'  # TODO: You map choice here. If left empty, the map 'training1' will be selected.

game_layer = GameLayer(api_key)


def write(filename, commands):
    with open(filename) as f:
        for command in commands:
            f.write(command)


def simple():
    filename = '\\games\\' +  map_name + str(time()).split('.')[0]
    commands = []

    game_layer.new_game(map_name)
    print('Starting game: ' + game_layer.game_state.game_id)
    game_layer.start_game()

    while game_layer.game_state.turn < game_layer.game_state.max_turns:
        commands.append(take_turn())

    print('Done with game: ' + game_layer.game_state.game_id)
    print('Final score was: ' + str(game_layer.get_score()['finalScore']))

    write(filename, commands)

def replay(filename):
    commands = []

    with open(filename) as f:
        commands.append(f.readline())

    #TODO

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
    pass #TODO


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
        else:
            die('Unknown command')

def take_turn():
    # TODO Implement your artificial intelligence here.
    # TODO Take one action per turn until the game ends.
    # TODO The following is a short example of how to use the StarterKit

    state = game_layer.game_state

    command = ''

    if len(state.residences) < 1:
        for i in range(len(state.map)):
            for j in range(len(state.map)):
                if state.map[i][j] == 0:
                    x = i
                    y = j
                    break

        command = game_layer.place_foundation((x, y), game_layer.game_state.available_residence_buildings[0].building_name)

    else:
        the_only_residence = state.residences[0]
        if the_only_residence.build_progress < 100:
            command = game_layer.build((the_only_residence.X, the_only_residence.Y))
        elif the_only_residence.health < 50:
            command = game_layer.maintenance((the_only_residence.X, the_only_residence.Y))
        elif the_only_residence.temperature < 18:
            blueprint = game_layer.get_residence_blueprint(the_only_residence.building_name)
            energy = blueprint.base_energy_need + 0.5 \
                     + (the_only_residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
                     - the_only_residence.current_pop * 0.04
            command =  game_layer.adjust_energy_level((the_only_residence.X, the_only_residence.Y), energy)
        elif the_only_residence.temperature > 24:
            blueprint = game_layer.get_residence_blueprint(the_only_residence.building_name)
            energy = blueprint.base_energy_need - 0.5 \
                     + (the_only_residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
                     - the_only_residence.current_pop * 0.04
            command = game_layer.adjust_energy_level((the_only_residence.X, the_only_residence.Y), energy)
        elif state.available_upgrades[0].name not in the_only_residence.effects:
            command =  game_layer.buy_upgrade((the_only_residence.X, the_only_residence.Y), state.available_upgrades[0].name)
        else:
            command = game_layer.wait()

    for message in game_layer.game_state.messages:
        print(message)
    for error in game_layer.game_state.errors:
        print('Error: ' + error)

    return command

if __name__ == '__main__':
    main()
