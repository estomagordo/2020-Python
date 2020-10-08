from collections import defaultdict
from math import isclose

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
        self.temperature_undershoot_bounce = settings['temperature_undershoot_bounce']
        self.build_order = settings['build_order']
        self.upgrade_order = settings['upgrade_order']
        self.action_order = settings['action_order']
        self.demolish_replacement = settings['demolish_replacement']
        self.latest_foundation = settings['latest_foundation']
        self.ideal_temperature = settings['ideal_temperature']
        self.temperature_undershoot = settings['temperature_undershoot']
        self.temperature_horizon = settings['temperature_horizon']
        
        self.demolished = None
        self.build_order_picks = set()
        self.mall_spaces, self.wind_turbine_spaces, self.park_spaces, self.housing_spaces = self.divide_spaces()

    def act(self):
        for action in self.action_order:
            if action == 'ReplaceDemolished':
                if self.demolished:
                    x, y = self.demolished
                    self.building_counts[self.demolish_replacement] += 1
                    self.demolished = None

                    return f'place_foundation {x} {y} {self.demolish_replacement}'

            if action == 'AdjustEnergy':
                adjustee = self.most_urgent_energy_changee()

                if adjustee:
                    energy_level, base_energy_need, current_level = self.adjust_energy(adjustee)
                    self.energy_adjustments[(adjustee.X, adjustee.Y)] = self.game_state.turn
                    new_level = energy_level if energy_level > base_energy_need else base_energy_need + (current_level - base_energy_need) * self.temperature_undershoot_bounce

                    return f'adjust_energy_level {adjustee.X} {adjustee.Y} {new_level}'

            if action == 'Maintain':
                for residence in self.game_state.residences:
                    if residence.health < self.repair_limit and self.should_repair(residence.building_name):
                        return f'maintenance {residence.X} {residence.Y}'

            if action == 'Build':
                for residence in self.game_state.residences:
                    if residence.build_progress < 100:
                        return f'build {residence.X} {residence.Y}'

                for utility in self.game_state.utilities:
                    if utility.build_progress < 100:
                        return f'build {utility.X} {utility.Y}'

            if action == 'Upgrade':
                upgrade, x, y = self.upgrade_suggestion()
    
                if upgrade:
                    return f'buy_upgrade {x} {y} {upgrade}'

            if action == 'PlaceFoundation':
                if self.game_state.funds >= self.purchase_threshold and self.game_state.turn <= self.latest_foundation:
                    for _, cost, name, x, y, order in self.build_choice():
                        if cost > self.game_state.funds:
                            break

                        if x >= 0:
                            self.build_order_picks.add(order)
                            return f'place_foundation {x} {y} {name}'

                        if name not in self.game_state.releases or self.game_state.releases[name] > self.game_state.turn:
                            continue

                        if not self.game_state.available_spaces():
                            break
                        
                        x, y = self.build_place(name)

                        if x == -1:
                            continue

                        self.building_counts[name] += 1
                        
                        return f'place_foundation {x} {y} {name}'

            if action == 'Demolish':
                if self.earliest_demolish <= self.game_state.turn <= self.latest_demolish and self.game_state.funds >= self.demolish_fund_limit and self.building_counts['HighRise'] < self.highrise_limit and self.game_state.housing_queue >= self.demolishing_queue_limit:
                    if self.building_counts['Apartments'] > 1:
                        for residence in self.game_state.residences:
                            if residence.building_name == 'Apartments':
                                self.building_counts['Apartments'] -= 1
                                self.demolished = (residence.X, residence.Y)

                                return f'demolish {residence.X} {residence.Y}'

            if action == 'Wait':
                return 'wait'
            

    def upgrade_threshold(self, upgrade):
        if upgrade == 'Charger':
            return self.charger_threshold()
        if upgrade == 'Insulation':
            return self.insulation_threshold()
        if upgrade == 'Playground':
            return self.playground_threshold()
        if upgrade == 'Regulator':
            return self.regulator_threshold()
        if upgrade == 'Caretaker':
            return self.caretaker_threshold()
        return self.solar_panel_threshold()

    def build_choice(self):
        if self.build_order:
            for pos, order in enumerate(self.build_order):
                if pos in self.build_order_picks:
                    continue
                
                choice = order.split()
                name = choice[2]
                x = int(choice[0])
                y = int(choice[1])

                if name not in self.game_state.releases or self.game_state.releases[name] > self.game_state.turn:
                    continue

                cost = [building for building in self.game_state.available_buildings if building.building_name == name][0].cost

                return [[-1, cost, name, x, y, pos]]
                
            return [[10**9, 10**9, '', -1, -1, -1]]            

        highrise = (self.highrise_threshold + self.highrise_step * (0 if self.game_state.turn > 665 else self.building_counts['HighRise']), 18000, 'HighRise', -1, -1, -1)
        modern = (self.modern_threshold + self.modern_step * (0 if self.game_state.turn > 665 else self.building_counts['ModernApartments']), 7100, 'ModernApartments', -1, -1, -1)
        apartments = (self.apartments_threshold + self.apartments_step * (0 if self.game_state.turn > 665 else self.building_counts['Apartments']), 5200, 'Apartments', -1, -1, -1)
        cabin = (self.cabin_threshold + self.cabin_step * (0 if self.game_state.turn > 665 else self.building_counts['Cabin']), 2500, 'Cabin', -1, -1, -1)
        environmental = (self.environmental_threshold + (0 if self.game_state.turn > 665 else self.environmental_step * self.building_counts['EnvironmentalHouse']), 9000, 'EnvironmentalHouse', -1, -1, -1)
        luxury = (self.luxury_threshold + self.luxury_step * (0 if self.game_state.turn > 665 else self.building_counts['LuxuryResidence']), 3400, 'LuxuryResidence', -1, -1, -1)
        park = (self.park_threshold + self.park_step * (0 if self.game_state.turn > 665 else self.building_counts['Park']), 3750, 'Park', -1, -1, -1)
        wind_turbine = (self.wind_turbine_threshold + (0 if self.game_state.turn > 665 else self.wind_turbine_step * self.building_counts['WindTurbine']), 7500, 'WindTurbine', -1, -1, -1)
        mall = (self.mall_threshold + self.mall_step * (0 if self.game_state.turn > 665 else self.building_counts['Mall']), 16000, 'Mall', -1, -1, -1)

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

    def upgrade_suggestion(self):
        for upgrade in self.upgrade_order:
            if self.game_state.funds >= self.upgrade_threshold(upgrade):
                for residence in self.game_state.residences:
                    if upgrade not in residence.effects:
                        if upgrade == 'Charger':
                            for utility in self.game_state.utilities:
                                if utility.building_name != 'Mall':
                                    continue
                                if 2 <= abs(residence.X - utility.X) + abs(residence.Y - utility.Y) <= 3:
                                    return upgrade, residence.X, residence.Y
                        else:
                            return upgrade, residence.X, residence.Y

        return '', -1, -1
    
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
        base_energy_need = [bp for bp in self.game_state.available_residence_buildings if bp.building_name == residence.building_name][0].base_energy_need + (1.8 if 'Charger' in residence.effects else 0.0)
        outdoor_temp = self.game_state.current_temp
        emissivity = [bp for bp in self.game_state.available_residence_buildings if bp.building_name == residence.building_name][0].emissivity * (0.6 if 'Insulation' in residence.effects else 1.0)
        current_pop = residence.current_pop

        current = residence.effective_energy_in

        def resulting_temperature(new_energy, current_temp, iterations):
            for _ in range(iterations):
                current_temp = current_temp + (new_energy - base_energy_need) * degrees_per_excess_mwh + degrees_per_pop * current_pop - (current_temp - outdoor_temp) * emissivity

            return current_temp

        lo = 0.0
        hi = 100.0
        restemp = resulting_temperature((lo + hi) / 2.0, residence.temperature, self.temperature_horizon)

        while not isclose(restemp, self.ideal_temperature):
            if restemp < self.ideal_temperature:
                lo = (lo + hi) / 2.0
            else:
                hi = (lo + hi) / 2.0

            restemp = resulting_temperature((lo + hi) / 2.0, residence.temperature, self.temperature_horizon)

        return (lo + hi) / 2.0, base_energy_need, current

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
            
            candidates.append((abs(self.ideal_temperature - residence.temperature), residence))

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
        
        while len(mall_spaces) < self.max_malls:
            for x, y in radius3:
                if not mall_spaces or not any(abs(mx - x) + abs(my - y) < 6 for (mx, my) in mall_spaces):
                    mall_spaces.append((x, y))
                    spaces.remove((x, y))
                    if len(mall_spaces) == self.max_malls:
                        break

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
