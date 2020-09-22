from imposters_mark.entities.player import Player


class Stats(object):
    def __init__(self):
        self.locations = []
        self.available_location = [
            'Dropship',
            'Electrical',
            'Security',
            'O2',
            'Communications',
            'Weapons',
            'Office',
            'Admin',
            'Storage',
            'Specimen Room',
            'Laboratory',
            'Boiler Room',
            'Decontamination'
        ]
        self.players = {}
        self.available_players = [
            'Akatosh'
        ]
        self.thread_count = 0

    def get_current_location(self) -> str:
        if len(self.locations) == 0:
            return ''

        return self.locations[-1]

    def append_location(self, location):
        if location in self.available_location and location != self.get_current_location():
            self.locations.append(location)

    def get_last_locations(self, count):
        if len(self.locations) == 0:
            return ''

        start_index = len(self.locations) - count
        if start_index < 0:
            start_index = 0

        last_locations = ''
        for i in range(len(self.locations)):
            if i >= start_index:
                if i == (len(self.locations) - 1):
                    last_locations += self.locations[i]
                else:
                    last_locations += f'{self.locations[i]} -> '

        return last_locations

    def append_player(self, player: Player):
        if player.name in self.available_players:
            self.players[player.name] = player

    def get_last_players(self, count):
        players_keys = list(self.players.keys())
        if len(players_keys) == 0:
            return ''

        start_index = len(players_keys) - count
        if start_index < 0:
            start_index = 0

        last_players = ''
        for i in range(len(players_keys)):
            if i >= start_index:
                if i == (len(players_keys) - 1):
                    last_players += self.players[players_keys[i]].name
                else:
                    last_players += f'{self.players[players_keys[i]].name} -> '

        return last_players

    def get_players_position(self):
        players_positions = []

        for key in self.players.keys():
            players_positions.append(self.players[key].position)

        return players_positions
