class GameState:
    def __init__(self, map_values):
        self.game_id = map_values['gameId']
        self.map_name = map_values['mapName']
        self.max_turns = map_values['maxTurns']
        self.max_temp = map_values['maxTemp']
        self.min_temp = map_values['minTemp']
        self.map = map_values['map']
        self.energy_levels = list(map(EnergyLevel, map_values['energyLevels']))
        self.available_residence_buildings = list(map(BlueprintResidenceBuilding, map_values['availableResidenceBuildings']))
        self.available_utility_buildings = list(map(BlueprintUtilityBuilding, map_values['availableUitlityBuildings']))
        self.available_upgrades = list(map(Upgrade, map_values['availableUpgrades']))
        self.effects = list(map(Effect, map_values['effects']))

        self.turn = 0
        self.funds = 0
        self.total_co2 = 0
        self.total_happiness = 0
        self.current_temp = 0
        self.queue_happiness = 0
        self.housing_queue = 0
        self.residences = []
        self.utilities = []
        self.errors = []
        self.messages = []

    def update_state(self, state):
        self.turn = state['turn']
        self.funds = state['funds']
        self.total_co2 = state['totalCo2']
        self.total_happiness = state['totalHappiness']
        self.current_temp = state['currentTemp']
        self.queue_happiness = state['queueHappiness']
        self.housing_queue = state['housingQueue']
        self.residences = list(map(Residence, state['residenceBuildings']))
        self.utilities = list(map(Utility, state['utilityBuildings']))
        self.errors = state['errors']
        self.messages = state['messages']


class EnergyLevel:
    def __init__(self, level_values):
        self.energy_threshold = level_values['energyThreshold']
        self.cost_per_mwh = level_values['costPerMwh']
        self.co2_per_mwh = level_values['tonCo2PerMwh']


class Blueprint:
    def __init__(self, blueprint):
        self.building_name = blueprint['buildingName']
        self.cost = blueprint['cost']
        self.co2_cost = blueprint['co2Cost']
        self.base_energy_need = blueprint['baseEnergyNeed']
        self.build_speed = blueprint['buildSpeed']
        self.type = blueprint['type']
        self.release_tick = blueprint['releaseTick']


class BlueprintUtilityBuilding(Blueprint):
    def __init__(self, blueprint_building):
        super().__init__(blueprint_building)
        self.effects = blueprint_building['effects']
        self.queue_increase = blueprint_building['queueIncrease']


class BlueprintResidenceBuilding(Blueprint):
    def __init__(self, blueprint_building):
        super().__init__(blueprint_building)
        self.max_pop = blueprint_building['maxPop']
        self.income_per_pop = blueprint_building['incomePerPop']
        self.emissivity = blueprint_building['emissivity']
        self.maintenance_cost = blueprint_building['maintenanceCost']
        self.decay_rate = blueprint_building['decayRate']
        self.max_happiness = blueprint_building['maxHappiness']


class Upgrade:
    def __init__(self, upgrade):
        self.name = upgrade['name']
        self.effect = upgrade['effect']
        self.cost = upgrade['cost']


class Effect:
    def __init__(self, effect):
        self.name = effect['name']
        self.radius = effect['radius']
        self.emissivity_multiplier = effect['emissivityMultiplier']
        self.decay_multiplier = effect['decayMultiplier']
        self.building_income_increase = effect['buildingIncomeIncrease']
        self.max_happiness_increase = effect['maxHappinessIncrease']
        self.mwh_production = effect['mwhProduction']
        self.base_energy_mwh_increase = effect['baseEnergyMwhIncrease']
        self.co2_per_pop_increase = effect['co2PerPopIncrease']
        self.decay_increase = effect['decayIncrease']


class Building:
    def __init__(self, building):
        self.building_name = building['buildingName']
        self.X = building['position']['x']
        self.Y = building['position']['y']
        self.effective_energy_in = building['effectiveEnergyIn']
        self.build_progress = building['buildProgress']
        self.can_be_demolished = building['canBeDemolished']
        self.effects = building['effects']


class Residence(Building):
    def __init__(self, residence):
        super().__init__(residence)
        self.current_pop = residence['currentPop']
        self.temperature = residence['temperature']
        self.requested_energy_in = residence['requestedEnergyIn']
        self.happiness_per_tick_per_pop = residence['happinessPerTickPerPop']
        self.health = residence['health']


class Utility(Building):
    def __init__(self, utility):
        super().__init__(utility)
