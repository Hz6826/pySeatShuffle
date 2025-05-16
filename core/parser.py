"""
Parsers
"""
import csv
import json

from model import *

class PeopleParser:
    """
    ### People Table Format
    File Format: csv
    with table head: name,prop_name_1,prop_name_2,...
    """
    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def parse(self, file_path):
        people = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            head = next(reader)
            for row in reader:
                properties = {}
                for i in range(1, len(row)):
                    properties[head[i]] = row[i]
                people.append(Person(row[0], properties))
        return people


class SeatTableParser:
    """
    ### Seat Table Format
    File Format: json
    {
        "name": "smth",  (optional)
        "size": [w, h],
        "seat_groups": [
            {
                "name": "smth",  (optional)
                "seats": [
                    {
                        name: "smth",  (optional)
                        pos: [x, y]
                    },
                    ...
                ]
            },
            ...
        ]
    }
    """
    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def parse(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        seat_groups = []
        for group in data['seat_groups']:
            seats = []
            for seat in group['seats']:
                seats.append(Seat(seat['pos'], seat.get('name', None)))
            seat_groups.append(SeatGroup(seats, group.get('name', None)))
        return SeatTable(seat_groups, data.get('size', None), data.get('name', None))


class RulesetParser:
    """
    ### Ruleset Format
    File Format: json
    {
        "rules": [
            {
                "t": "smth",
                "prop": [
                    "smth",
                    "smth",
                    ...
                ],
                "reversed": true  (optional)
            },
            ...
        ],
        "relations": WIP
    """
    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def parse(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        rules = []
        for _rule in data['rules']:
            rules.append(Rule(_rule['t'], _rule['prop'], _rule.get('reversed', False)))
        return Ruleset(rules, data.get('relations', None))


default_people_parser = PeopleParser()
default_seat_table_parser = SeatTableParser()
default_ruleset_parser = RulesetParser()

def parse_people(file_path):
    return default_people_parser.parse(file_path)

def parse_seat_table(file_path):
    return default_seat_table_parser.parse(file_path)

def parse_ruleset(file_path):
    return default_ruleset_parser.parse(file_path)
