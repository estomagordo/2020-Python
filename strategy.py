from collections import defaultdict

class Strategy:
    def __init__(self, game_state, settings):
        self.game_state = game_state
        self.energy_adjustments = defaultdict(int)
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
        self.max_wind_turbines = settings['max_wind_turbines']
        self.max_parks = settings['max_parks']
        self.lower_upgrade_threshold = settings['lower_upgrade_threshold']
        self.lower_insulation_threshold = settings['lower_insulation_threshold']
        self.lower_playground_threshold = settings['lower_playground_threshold']
        self.lower_solar_panel_threshold = settings['lower_solar_panel_threshold']
        self.lower_regulator_threshold = settings['lower_regulator_threshold']
        self.lower_caretaker_threshold = settings['lower_caretaker_threshold']
        self.lower_charger_threshold = settings['lower_charger_threshold']
        self.highrise_limit = settings['highrise_limit']
        self.energy_change_cooldown = settings['energy_change_cooldown']
        self.temp_diff_freakout_cutoff = settings['temp_diff_freakout_cutoff']
        self.temp_diff_freakout_factor = settings['temp_diff_freakout_factor']
        self.mall_weight = settings['mall_weight']
        self.wind_turbine_weight = settings['wind_turbine_weight']
        self.park_weight = settings['park_weight']
        self.residence_weight = settings['residence_weight']
        self.residence_weight_length = settings['residence_weight_length']
        self.target_temp = settings['target_temp']
        self.temperature_dampening_factor = settings['temperature_dampening_factor']
        self.start_upgrading_turn = settings['start_upgrading_turn']
        self.earliest_demolish = settings['earliest_demolish']
        self.latest_demolish = settings['latest_demolish']
        self.demolish_fund_limit = settings['demolish_fund_limit']
        self.demolishing_queue_limit = settings['demolishing_queue_limit']
        
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

        choices = []

        if len(self.game_state.residences) < self.max_residences:
            choices.append(modern)
            choices.append(apartments)
            choices.append(cabin)
            choices.append(environmental)
            choices.append(luxury)

            if self.building_counts['HighRise'] < self.highrise_limit:
                choices.append(highrise)

        if self.building_counts['Park'] < self.max_parks:
            choices.append(park)

        if self.building_counts['WindTurbine'] < self.max_wind_turbines:
            choices.append(wind_turbine)

        if self.building_counts['Mall'] < self.max_malls:
            choices.append(mall)
        
        return sorted(choices)

    def charger_threshold(self):
        if self.game_state.turn < self.start_upgrading_turn:
            return 10**9

        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_charger_threshold

        return self.charger_base_threshold

    def caretaker_threshold(self):
        if self.game_state.turn < self.start_upgrading_turn:
            return 10**9
            
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_caretaker_threshold

        return self.caretaker_base_threshold

    def insulation_threshold(self):
        if self.game_state.turn < self.start_upgrading_turn:
            return 10**9
            
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_insulation_threshold

        return self.insulation_base_threshold

    def regulator_threshold(self):
        if self.game_state.turn < self.start_upgrading_turn:
            return 10**9
            
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_regulator_threshold

        return self.regulator_base_threshold

    def playground_threshold(self):
        if self.game_state.turn < self.start_upgrading_turn:
            return 10**9
            
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_playground_threshold

        return self.playground_base_threshold

    def solar_panel_threshold(self):
        if self.game_state.turn < self.start_upgrading_turn:
            return 10**9
            
        if self.game_state.turn >= self.lower_upgrade_threshold:
            return self.lower_solar_panel_threshold

        return self.solar_panel_base_threshold
    
    def build_place(self, name):
        if name == 'Mall':
            best = [-1, -1, -1]

            for x, y in self.game_state.available_spaces():
                count = 0

                for residence in self.game_state.residences:
                    if abs(x - residence.X) + abs(y - residence.Y) > 3:
                        continue

                    good = True

                    for utility in self.game_state.utilities:
                        if utility.building_name != 'Mall':
                            continue

                        if abs(utility.X - residence.X) + abs(utility.Y - residence.Y) <= 3:
                            good = False
                            break

                    if good:
                        count += 1

                if count > best[0]:
                    best = [count, x, y]

            return best[1:]

        if name in ('WindTurbine', 'Park'):
            best = [-1, -1, -1]

            for x, y in self.game_state.available_spaces():
                if (x, y) in self.mall_spaces:
                    continue
                
                count = 0

                for residence in self.game_state.residences:
                    if abs(x - residence.X) + abs(y - residence.Y) > 2:
                        continue

                    good = True

                    for utility in self.game_state.utilities:
                        if utility.building_name != name:
                            continue

                        if abs(utility.X - residence.X) + abs(utility.Y - residence.Y) <= 2:
                            good = False
                            break

                    if good:
                        count += 1

                if count > best[0]:
                    best = [count, x, y]

            return best[1:]

        best = [-1, -1, -1]

        for x, y in self.game_state.available_spaces():
            if (x, y) in self.mall_spaces:
                continue

            weight = 0

            for utility in self.game_state.utilities:
                if abs(x - utility.X) + abs(y - utility.Y) <= 2:
                    weight += self.mall_weight if utility.building_name == 'Mall' else self.wind_turbine_weight if utility.building_name == 'WindTurbine' else self.park_weight

            for residence in self.game_state.residences:
                if abs(x - residence.X) + abs(y - residence.Y) <= self.residence_weight_length:
                    weight += self.residence_weight
            
            if weight > best[0]:
                best = [weight, x, y]

        return best[1:]
    
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

    def adjust_energy(self, residence):
        degrees_per_pop = 0.04
        degrees_per_excess_mwh = 0.75
        base_energy_need = [bp for bp in self.game_state.available_residence_buildings if bp.building_name == residence.building_name][0].base_energy_need
        outdoor_temp = self.game_state.current_temp
        emissivity = [bp for bp in self.game_state.available_residence_buildings if bp.building_name == residence.building_name][0].emissivity * (0.6 if 'Insulation' in residence.effects else 1.0)

        current = residence.effective_energy_in
        target = (-residence.temperature + base_energy_need * degrees_per_excess_mwh - degrees_per_pop * residence.current_pop + residence.temperature * emissivity - outdoor_temp * emissivity + self.target_temp) / degrees_per_excess_mwh

        result = current + (target - current) / self.temperature_dampening_factor

        return result, base_energy_need

    def base_energy_need_for_building(self, name):
        for blueprint in self.game_state.available_residence_buildings:
            if blueprint.building_name == name:
                return blueprint.base_energy_need

    def most_urgent_energy_changee(self):
        candidates = []

        for residence in self.game_state.residences:
            if self.energy_adjustments[(residence.X, residence.Y)] + self.energy_change_cooldown > self.game_state.turn:
                continue
            if self.low_temp <= residence.temperature <= self.high_temp:
                continue
            if residence.temperature > self.high_temp and residence.requested_energy_in == self.base_energy_need_for_building(residence.building_name):
                continue
            
            candidates.append((abs(21.0 - residence.temperature), residence))

        if not candidates:
            return None

        candidates.sort(key=lambda candidate:-candidate[0])

        return candidates[0][1]

    def lower_energy(self, diff):
        factor = self.temp_diff_freakout_factor if diff > self.temp_diff_freakout_cutoff else 1.0

        return factor * self.energy_downstep

    def increase_energy(self, diff):
        factor = self.temp_diff_freakout_factor if diff > self.temp_diff_freakout_cutoff else 1.0

        return factor * self.energy_upstep

    def divide_spaces(self):
        spaces = set(self.game_state.available_spaces())

        housing_spaces = [] 
        mall_spaces = []
        wind_turbine_spaces = []
        park_spaces = []

        radius3 = sorted([pair for pair in spaces], key=lambda pair: -self.inrange(pair[0], pair[1], 3))
        radius2 = sorted([pair for pair in spaces], key=lambda pair: -self.inrange(pair[0], pair[1], 2))
        
        for x in range(self.max_malls):
            spaces.remove(radius3[x])
            mall_spaces.append(radius3[x])

        for x in range(self.max_wind_turbines):
            if radius2[x] not in spaces:
                continue
            spaces.remove(radius2[x])
            wind_turbine_spaces.append(radius2[x])

        for x in range(self.max_parks):
            if radius2[x] not in spaces:
                continue
            spaces.remove(radius2[x])
            park_spaces.append(radius2[x])

        for pair in radius3:
            if pair in spaces:
                housing_spaces.append(pair)

        return mall_spaces, wind_turbine_spaces, park_spaces, housing_spaces
