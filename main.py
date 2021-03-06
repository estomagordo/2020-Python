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

map_name = ''

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
    print(f'Final score was: {str(game_layer.get_score()["finalScore"])}\n')
    
    write(filename, commands)

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
            if game == 0 and game_layer.game_state.turn == 0:
                print(game_layer.game_state)

            command = strategy.act()
            commands.append(command)
            
            game_layer.translate(command.split())
            
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

    if mode == 'endall':
        endall()
    elif len(argv) == 2:
        die('Supply map number!')
    else:        
        map_number = argv[2]
        map_name += map_number
        
        if mode == 'latest':
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

if __name__ == '__main__':
    main()
