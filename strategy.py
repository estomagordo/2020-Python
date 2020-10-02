from collections import defaultdict

class Strategy:
    def __init__(self, game_state, settings):
        self.game_state = game_state
        self.energy_adjustments = {}
        self.building_counts = defaultdict(int)
        self.insulation_base_threshold = settings['insulation_threshold']
        self.playground_base_threshold = settings['playground_threshold']
        self.solar_panel_base_threshold = settings['solar_panel_threshold']
        self.regulator_base_threshold = settings['regulator_threshold']
        self.caretaker_base_threshold = settings['caretaker_threshold']
        self.charger_base_threshold = settings['charger_threshold']
        self.waiting_limit = settings['waiting_limit']
        self.repair_limit = settings['repair_limit']
        self.highrise_threshold = settings['highrise_threshold']
        self.highrise_step = settings['highrise_step']        
        self.modern_threshold = settings['modern_threshold']
        self.modern_step = settings['modern_step']
        self.apartments_threshold = settings['apartments_threshold']
        self.apartments_step = settings['apartments_step']
        self.cabin_threshold = settings['cabin_threshold']
        self.cabin_step = settings['cabin_step']
        self.environmental_threshold = settings['environmental_threshold']
        self.environmental_step = settings['environmental_step']
        self.luxury_threshold = settings['luxury_threshold']
        self.luxury_step = settings['luxury_step']
        self.park_threshold = settings['park_threshold']
        self.park_step = settings['park_step']
        self.wind_turbine_threshold = settings['wind_turbine_threshold']
        self.wind_turbine_step = settings['wind_turbine_step']
        self.mall_threshold = settings['mall_threshold']
        self.mall_step = settings['mall_step']
        self.max_residences = settings['max_residences']
        self.low_temp = settings['low_temp']
        self.high_temp = settings['high_temp']
        self.energy_upstep = settings['energy_upstep']
        self.energy_downstep = settings['energy_downstep']
        self.maintenance_highrise = settings['maintenance_highrise']
        self.maintenance_apartments = settings['maintenance_apartments']
        self.maintenance_modern = settings['maintenance_modern']
        self.maintenance_cabin = settings['maintenance_cabin']
        self.maintenance_luxury = settings['maintenance_luxury']
        self.maintenance_environmental = settings['maintenance_environmental']
        self.purchase_threshold = settings['purchase_threshold']
        self.max_malls = settings['max_malls']
        self.max_wind_mills = settings['max_wind_mills']
        self.max_parks = settings['max_parks']
        self.lower_upgrade_threshold = settings['lower_upgrade_threshold']
        self.lower_insulation_threshold = settings['lower_insulation_threshold']
        self.lower_playground_threshold = settings['lower_playground_threshold']
        self.lower_solar_panel_threshold = settings['lower_solar_panel_threshold']
        self.lower_regulator_threshold = settings['lower_regulator_threshold']
        self.lower_caretaker_threshold = settings['lower_caretaker_threshold']
        self.lower_charger_threshold = settings['lower_charger_threshold']
        self.highrise_limit = settings['highrise_limit']

        self.mall_spaces, self.wind_turbine_spaces, self.park_spaces, self.housing_spaces = self.divide_spaces()

    def build_choice(self):
        highrise = (self.highrise_threshold + self.highrise_step * (0 if self.game_state.turn > 665 else self.building_counts['HighRise']), 18000, 'HighRise')
        modern = (self.modern_threshold + self.modern_step * (0 if self.game_state.turn > 665 else self.building_counts['ModernApartments']), 7100, 'ModernApartments')
        apartments = (self.apartments_threshold + self.apartments_step * (0 if self.game_state.turn > 665 else self.building_counts['Apartments']), 5200, 'Apartments')
        cabin = (self.cabin_threshold + self.cabin_step * (0 if self.game_state.turn > 665 else self.building_counts['Cabin']), 2500, 'Cabin')
        environmental = (self.environmental_threshold + (0 if self.game_state.turn > 665 else self.environmental_step * self.building_counts['EnvironmentalHouse']), 9000, 'EnvironmentalHouse')
        luxury = (self.luxury_threshold + self.luxury_step * (0 if self.game_state.turn > 665 else self.building_counts['LuxuryResidence']), 3400, 'LuxuryResidence')
        park = (self.park_threshold + self.park_step * (0 if self.game_state.turn > 665 else self.building_counts['Park']), 3750, 'Park')
        wind_turbine = (self.wind_turbine_threshold + (0 if self.game_state.turn > 665 else self.wind_turbine_step * self.building_counts['WindTurbine']), 7500, 'WindTurbine')
        mall = (self.mall_threshold + self.mall_step * (0 if self.game_state.turn > 665 else self.building_counts['Mall']), 16000, 'Mall')

        return sorted([b for b in (highrise, modern, apartments, cabin, environmental, luxury, park, wind_turbine, mall)])

    def charger_threshold(self):
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_charger_threshold

        return self.charger_base_threshold

    def caretaker_threshold(self):
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_caretaker_threshold

        return self.caretaker_base_threshold

    def insulation_threshold(self):
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_insulation_threshold

        return self.insulation_base_threshold

    def regulator_threshold(self):
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_regulator_threshold

        return self.regulator_base_threshold

    def playground_threshold(self):
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_playground_threshold

        return self.playground_base_threshold

    def solar_panel_threshold(self):
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_solar_panel_threshold

        return self.solar_panel_base_threshold
    
    def build_place(self, name):
        if name == 'Mall':
            for x, y in self.mall_spaces:
                if self.game_state.map[x][y] == 0:
                    return x, y

        if name == 'WindMill':
            for x, y in self.wind_turbine_spaces:
                if self.game_state.map[x][y] == 0:
                    return x, y

        if name == 'Park':
            for x, y in self.park_spaces:
                if self.game_state.map[x][y] == 0:
                    return x, y

        for x, y in self.housing_spaces:
            if self.game_state.map[x][y] == 0:
                return x, y

        return -1, -1
    
    def should_repair(self, name):
        limit = {
            'HighRise': self.maintenance_highrise,
            'Apartments': self.maintenance_apartments,
            'ModernApartments': self.maintenance_modern,
            'Cabin': self.maintenance_cabin,
            'EnvironmentalHouse': self.maintenance_environmental,
            'LuxuryResidence': self.maintenance_luxury
        }

        return self.game_state.funds >= limit[name]

    def inrange(self, x, y, radius):
        count = 0

        for nx in range(len(self.game_state.map)):
            for ny in range(len(self.game_state.map[nx])):
                if nx == x and ny == y:
                    continue

                if abs(nx - x) + abs(ny - y) > radius:
                    continue

                if self.game_state.map[nx][ny] != 1:
                    count += 1

        return count

    def divide_spaces(self):
        spaces = set(self.game_state.available_spaces())

        housing_spaces = [] 
        mall_spaces = []
        wind_mill_spaces = []
        park_spaces = []

        radius3 = sorted([pair for pair in spaces], key=lambda pair: -self.inrange(pair[0], pair[1], 3))
        radius2 = sorted([pair for pair in spaces], key=lambda pair: -self.inrange(pair[0], pair[1], 2))
        
        for x in range(self.max_malls):
            spaces.remove(radius3[x])
            mall_spaces.append(radius3[x])

        for x in range(self.max_wind_mills):
            if radius2[x] not in spaces:
                continue
            spaces.remove(radius2[x])
            wind_mill_spaces.append(radius2[x])

        for x in range(self.max_parks):
            if radius2[x] not in spaces:
                continue
            spaces.remove(radius2[x])
            park_spaces.append(radius2[x])

        for pair in radius3:
            if pair in spaces:
                housing_spaces.append(pair)

        return mall_spaces, wind_mill_spaces, park_spaces, housing_spaces
