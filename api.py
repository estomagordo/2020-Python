import requests

from requests import RequestException

base_api_path = 'https://game.considition.com/api/game/'

class Api:
    def __init__(self, api_key):
        self.api_key = api_key
        self.sess = requests.Session()
        self.game_id= ''

    def set_game_id(self, game_id):
        self.game_id = game_id

    def new_game(self, game_options=''):
        try:        
            response = self.sess.post(base_api_path + 'new', json=game_options, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not create new game')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not create new game')
            print('Something went wrong with the request: ' + str(e))

    def start_game(self, game_id=''):
        try:
            response = self.sess.get(base_api_path + 'start?GameId=' + self.game_id, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not start game')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not start game')
            print('Something went wrong with the request: ' + str(e))

    def end_game(self, game_id=''):
        try:
            response = self.sess.get(base_api_path + 'end?GameId=' + self.game_id, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return

            print('Fatal Error: could not end game')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not end game')
            print('Something went wrong with the request: ' + str(e))

    def get_score(self, game_id=''):
        try:
            response = self.sess.get(base_api_path + 'score?GameId=' + self.game_id, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not get score')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not get score')
            print('Something went wrong with the request: ' + str(e))

    def get_game_info(self, game_id=''):
        try:
            response = self.sess.get(base_api_path + 'gameInfo?GameId=' + self.game_id, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not get game info')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not get game info')
            print('Something went wrong with the request: ' + str(e))        

    def place_foundation(self, foundation, game_id=''):
        try:
            response = self.sess.post(base_api_path + 'action/startBuild?GameId=' + self.game_id, json=foundation, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not do action place foundation')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not do action place foundation')
            print('Something went wrong with the request: ' + str(e))

    def build(self, pos, game_id=''):
        try:
            response = self.sess.post(base_api_path + 'action/Build?GameId=' + self.game_id, json=pos, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not do action build')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not do action build')
            print('Something went wrong with the request: ' + str(e))

    def maintenance(self, pos, game_id=''):
        try:
            response = self.sess.post(base_api_path + 'action/maintenance?GameId=' + self.game_id, json=pos, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not do action maintenance')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not do action maintenance')
            print('Something went wrong with the request: ' + str(e))

    def demolish(self, pos, game_id=''):
        try:
            response = self.sess.post(base_api_path + 'action/demolish?GameId=' + self.game_id, json=pos, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not do action demolish')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not do action demolish')
            print('Something went wrong with the request: ' + str(e))

    def wait(self, game_id=''):
        try:
            response = self.sess.post(base_api_path + 'action/wait?GameId=' + self.game_id, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not do action wait')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not do action wait')
            print('Something went wrong with the request: ' + str(e))

    def adjust_energy(self, energy_level, game_id=''):
        try:
            response = self.sess.post(base_api_path + 'action/adjustEnergy?GameId=' + self.game_id, json=energy_level, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json() 
            print('Fatal Error: could not do action adjust energy level')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not do action adjust energy level')
            print('Something went wrong with the request: ' + str(e))

    def buy_upgrades(self, upgrade, game_id=''):
        try:
            response = self.sess.post(base_api_path + 'action/buyUpgrade?GameId=' + self.game_id, json=upgrade, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not do action buy upgrades')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not do action buy upgrades')
            print('Something went wrong with the request: ' + str(e))

    def get_game_state(self):
        try:
            response = self.sess.get(base_api_path + 'gameState?GameId=' + self.game_id, headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not get game state')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not do get game state')
            print('Something went wrong with the request: ' + str(e))

    def get_games(self):
        try:
            response = self.sess.get(base_api_path + 'games', headers={'x-api-key': self.api_key})
            if response.status_code == 200:
                return response.json()

            print('Fatal Error: could not get games')
            print(str(response.status_code) + ' ' + response.reason + ': ' + response.text)
        except RequestException as e:
            print('Fatal Error: could not get games')
            print('Something went wrong with the request: ' + str(e))
