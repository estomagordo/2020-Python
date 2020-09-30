from collections import defaultdict

class Strategy:
    def __init__(self, game_state, settings):
        self.game_state = game_state
        self.energy_adjustments = {}
        self.building_counts = defaultdict(int)
        self.insulation_threshold = settings['insulation_threshold']
        self.playground_threshold = settings['playground_threshold']
        self.solar_panel_threshold = settings['solar_panel_threshold']
        self.regulator_threshold = settings['regulator_threshold']
        self.waiting_limit = settings['waiting_limit']
        self.repair_limit = settings['repair_limit']
        self.highrise_threshold = settings['highrise_threshold']
        self.highrise_step = settings['highrise_step']        
        self.modern_threshold = settings['modern_threshold']
        self.modern_step = settings['modern_step']
        self.apartments_threshold = settings['apartments_threshold']
        self.apartments_step = settings['apartments_step']
        self.park_threshold = settings['park_threshold']
        self.park_step = settings['park_step']
        self.wind_turbine_threshold = settings['wind_turbine_threshold']
        self.wind_turbine_step = settings['wind_turbine_step']
        self.mall_threshold = settings['mall_threshold']
        self.mall_step = settings['mall_step']
        self.max_residences = settings['max_residences']
        self.low_temp = settings['low_temp']
        self.high_temp = settings['high_temp']
        self.energy_step = settings['energy_step']

    def build_choice(self):
        highrise = (self.highrise_threshold + self.highrise_step * self.building_counts['HighRise'], 'HighRise')
        modern = (self.modern_threshold + self.modern_step * self.building_counts['ModernApartments'], 'ModernApartments')
        apartments = (self.apartments_threshold + self.apartments_step * self.building_counts['Apartments'], 'Apartments')
        park = (self.park_threshold + self.park_step * self.building_counts['Park'], 'Park')
        wind_turbine = (self.wind_turbine_threshold + self.wind_turbine_step * self.building_counts['WindTurbine'], 'WindTurbine')
        mall = (self.mall_threshold + self.mall_step * self.building_counts['Mall'], 'Mall')

        return sorted([b for b in (highrise, modern, apartments, park, wind_turbine, mall) if b[0] <= self.game_state.funds])