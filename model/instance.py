"""
Instance Model
"""
from .ruleset import *
from .seat_table import *
from .person import *


class Instance:
    def __init__(self, name: str, people: list[Person], seat_table: SeatTable, ruleset: Ruleset):
        self.name = name
        self.people = people
        self.seat_table = seat_table
        self.ruleset = ruleset
